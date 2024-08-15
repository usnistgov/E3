package gov.nist.eee.pipeline.discounted;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.object.input.TimestepComp;
import gov.nist.eee.object.tree.Tree;
import gov.nist.eee.output.ResultOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.discounted.presentvalue.ContinuousPresentValue;
import gov.nist.eee.pipeline.discounted.presentvalue.EndOfYearPresentValue;
import gov.nist.eee.pipeline.discounted.presentvalue.MidYearPresentValue;
import gov.nist.eee.pipeline.discounted.presentvalue.PresentValueFormula;
import gov.nist.eee.pipeline.residualvalue.ResidualValuePipeline;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.Stream;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

@Pipeline(name = "discounted", dependencies = {ResidualValuePipeline.class})
@OutputMapper(ResultOutputMapper.class)
public class DiscountedPipeline
        extends CellPipeline<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>
        implements IWithDependency, IWithAssignableInputs {
    private Logger logger = LoggerFactory.getLogger(DiscountedPipeline.class);

    private Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> cValues;
    private Cell<Double> cDiscountRate;
    private Cell<PresentValueFormula> cPresentValueFormula;

    private Cell<CellSink<Double>> cDiscountReal;
    private Cell<CellSink<Double>> cDiscountNominal;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up discounted pipeline");

        var sAnalysis = sInput.map(Input::analysis);

        var sOutputReal = sAnalysis.map(Analysis::outputReal);
        cDiscountReal = sAnalysis.map(Analysis::discountRateReal).map(CellSink::new).hold(new CellSink<>(0.0));
        cDiscountNominal = sAnalysis.map(Analysis::discountRateNominal).map(CellSink::new).hold(new CellSink<>(0.0));

        cDiscountRate = sOutputReal.hold(true).lift(
                Cell.switchC((Cell) cDiscountReal),
                Cell.switchC((Cell) cDiscountNominal),
                (isReal, real, nominal) -> isReal ? real : nominal
        );

        cPresentValueFormula = sAnalysis.map(Analysis::timestepComp)
                .hold(TimestepComp.END_OF_YEAR)
                .map(DiscountedPipeline::getPresentValueFormula);
    }

    @Override
    public Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> define() {
        logger.trace("Defining discounted pipeline");

        return cValues.lift(
                cDiscountRate,
                cPresentValueFormula,
                (values, discountRate, presentValueFormula) -> values.map(v -> {
                    var result = new HashMap<Integer, Cell<List<Double>>>();

                    for (var entry : v.entrySet()) {
                        result.put(
                                entry.getKey(),
                                entry.getValue().map(entryValue ->
                                        discountValues(entryValue, discountRate, presentValueFormula)
                                )
                        );
                    }

                    return result;
                })
        );
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for discounted pipeline. " + parameters);

        cValues = parameters.get(ResidualValuePipeline.class);
    }

    @Override
    public Cell<Model> getAssignableInputs() {
        logger.trace("Creating assignable inputs for discounted pipeline");

        return Util.createInputModel(
                cDiscountReal.lift(cDiscountNominal, DiscountedPipeline::addDoubleInputs),
                new Cell<>(integerInputs -> {
                })
        );
    }

    private static Consumer<Tree<String, CellSink<Double>>> addDoubleInputs(
            CellSink<Double> cDiscountRateReal,
            CellSink<Double> cDiscountRateNominal
    ) {
        return doubleInputs -> {
            doubleInputs.add(new String[]{"analysisObject", "discountRateReal"}, cDiscountRateReal);
            doubleInputs.add(new String[]{"analysisObject", "discountRateNominal"}, cDiscountRateNominal);
        };
    }


    /**
     * Gets the matching present value formula based on the time-step comp.
     *
     * @param timestepComp the time-step comp of the current model.
     * @return the present value functional interface that corresponds to the given time-step comp.
     */
    public static PresentValueFormula getPresentValueFormula(@Nullable TimestepComp timestepComp) {
        if (timestepComp == null)
            return new EndOfYearPresentValue();

        return switch (timestepComp) {
            case END_OF_YEAR -> new EndOfYearPresentValue();
            case MID_YEAR -> new MidYearPresentValue();
            case CONTINUOUS -> new ContinuousPresentValue();
        };
    }

    /**
     * Calculates the discounted values form the given values list, discount rate, and present value formula.
     *
     * @param values  the values to discount.
     * @param rate    the discount rate.
     * @param formula the present value formula to apply.
     * @return a list of discount values.
     */
    public static List<Double> discountValues(List<Double> values, double rate, PresentValueFormula formula) {
        var result = new ArrayList<Double>(values.size());

        for (int i = 0; i < values.size(); i++) {
            result.add(formula.presentValue(values.get(i), rate, i));
        }

        return result;
    }
}
