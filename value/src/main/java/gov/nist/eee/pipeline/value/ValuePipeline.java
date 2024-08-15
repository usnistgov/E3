package gov.nist.eee.pipeline.value;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Bcn;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.object.input.VarRate;
import gov.nist.eee.output.ResultOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;
import java.util.Objects;

import static gov.nist.eee.pipeline.quantity.QuantityPipeline.inflateVarValue;
import static gov.nist.eee.pipeline.quantity.QuantityPipeline.mapWithVarRate;

/**
 * The value pipeline transforms BCN quantity values from {@link QuantityPipeline} their monetary values with the
 * BCNs value per quantity property.
 */
@Pipeline(name = "values", dependencies = {QuantityPipeline.class}, inputDependencies = {QuantityPipeline.class})
@OutputMapper(ResultOutputMapper.class)
public class ValuePipeline
        extends CellPipeline<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>
        implements IWithDependency, IWithAssignableInputs, IWithInput {
    private static final Logger logger = LoggerFactory.getLogger(ValuePipeline.class);

    /**
     * The study period of the current request.
     */
    private Cell<Integer> cStudyPeriod;

    /**
     * The quantity values for each BCN from {@link QuantityPipeline}.
     */
    private Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> cQuantities;

    /**
     * The value per quantity values for each BCN retrieved from the input BCNs.
     */
    private Cell<Map<Integer, CellSink<Double>>> cValuePerQ;

    /**
     * The var values for each BCN retrieved from the input BCNs.
     */
    private Cell<Map<Integer, List<Double>>> cVarValue;

    /**
     * The var rate for each BCN retrieved from the input BCNs.
     */
    private Cell<Map<Integer, VarRate>> cVarRate;

    /**
     * Create the assignable inputs for this {@link ValuePipeline}.
     *
     * @return A cell containing the assignable input {@link Model}.
     */
    @Override
    public Cell<Model> getAssignableInputs() {
        logger.trace("Creating assignable inputs for value pipeline");

        return Util.createInputModel(
                cValuePerQ.map(map -> doubleInputs -> Util.addMapToTree(map, doubleInputs, "bcnObjects.%d.quantityValue")),
                new Cell<>(integerInputs -> {
                })
        );
    }

    /**
     * Sets up this {@link ValuePipeline} by retrieved request invariable objects from the input stream.
     *
     * @param sInput     the main input stream which contains Input objects.
     */
    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up value pipeline");

        var cBcns = sInput.map(Input::bcnObjects).hold(List.of());

        cValuePerQ = Util.toSinkMap(cBcns, Bcn::id, Bcn::quantityValue);
        cVarValue = Util.toMap(cBcns, Bcn::id, bcn -> bcn.recur() == null ? null : bcn.recur().varValue());
        cVarRate = Util.toMap(cBcns, Bcn::id, bcn -> bcn.recur() == null ? null : bcn.recur().varRate());
    }

    @Override
    public void setupInput(Cell<Model> cModel) {
        logger.debug("Setup input for value pipeline");

        cStudyPeriod = Cell.switchC(cModel.map(model -> model.intInputs().get(new String[]{"analysisObject", "studyPeriod"})));
    }

    /**
     * Defines this {@link ValuePipeline}.
     *
     * @return A cell containing a map of BCN IDs to cells containing lists of values.
     */
    @Override
    public Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> define() {
        logger.trace("Defining value pipeline");

        return cQuantities.lift(cValuePerQ, cVarValue, cVarRate, cStudyPeriod, (quantityResult, valuePerQs, varValues, varRates, studyPeriod) ->
                quantityResult.flatMap((quantities) ->
                        Util.resultSequence(Util.combineMap(quantities, valuePerQs, varValues, varRates,
                                (v1, v2, v3, v4) -> ValuePipeline.calculateValues(v1, v2, v3, v4, studyPeriod)
                        ))
                )
        );
    }

    /**
     * Sets up the pipeline dependencies for this {@link ValuePipeline}.
     * Depends on {@link QuantityPipeline}.
     *
     * @param parameters The pipeline parameters containing the dependencies.
     */
    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for value pipeline. " + parameters);

        cQuantities = parameters.get(QuantityPipeline.class);
    }

    /**
     * Predicate that determines whether the values can be created directory or if the values need to be inflated first.
     *
     * @param varValue the list of values in the BCN.
     * @param varRate  the var rate of the BCN.
     * @return true if the values need to be inflated, otherwise false.
     */
    public static boolean shouldUseVarRateMap(List<Double> varValue, VarRate varRate) {
        return Objects.nonNull(varValue) && Objects.nonNull(varRate);
    }

    /**
     * Decide between inflating values or just using the quantity values directly.
     *
     * @param quantity    The list of quantities gotten from {@link QuantityPipeline}.
     * @param valuePerQ   The monetary value per quantity retrieved from the BCN.
     * @param varValue    The var values retrieved from the BCN.
     * @param varRate     The var rate retrieved from the BCN.
     * @param studyPeriod The length of the study period for the current analysis.
     * @return The list of values created from one of two methods.
     */
    public static Result<Cell<List<Double>>, E3Exception> calculateValues(
            Cell<List<Double>> quantity,
            Cell<Double> valuePerQ,
            List<Double> varValue,
            VarRate varRate,
            int studyPeriod
    ) {
        if (shouldUseVarRateMap(varValue, varRate))
            return getUsingVarRateMap(quantity, valuePerQ, varValue, varRate, studyPeriod);

        return new Result.Success<>(multiplyByValue(quantity, valuePerQ));
    }

    /**
     * Calculate values by inflating and mapping with the var rate.
     *
     * @param quantity    The quantity values to base the values on.
     * @param cValuePerQ  The monetary value per quantity retrieved from the BCN.
     * @param varValue    The var values retrieved from the BCN.
     * @param varRate     The var rate retrieved from the BCN.
     * @param studyPeriod The length of the study period for the current analysis.
     * @return The list of values created by inflating and mapping with the var rate.
     */
    public static Result<Cell<List<Double>>, E3Exception> getUsingVarRateMap(
            Cell<List<Double>> quantity,
            Cell<Double> cValuePerQ,
            List<Double> varValue,
            VarRate varRate,
            int studyPeriod
    ) {
        return inflateVarValue(varValue, studyPeriod + 1)
                .map(value -> mapWithVarRate(value, varRate))
                .map(values -> quantity
                        .map(q -> Util.elementwiseMultiply(values, q))
                        .lift(cValuePerQ, Util::multiplier)
                );
    }

    /**
     * Multiples every value in the list by the given value per quantity.
     *
     * @param cValues    The values to modify.
     * @param cValuePerQ The value to multiply the elements in the list by.
     * @return a Cell with the list of modified values.
     */
    public static Cell<List<Double>> multiplyByValue(Cell<List<Double>> cValues, Cell<Double> cValuePerQ) {
        return cValues.lift(cValuePerQ, Util::multiplier);
    }
}
