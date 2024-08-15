package gov.nist.eee.pipeline.quantity;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Bcn;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.object.input.VarRate;
import gov.nist.eee.object.tree.Tree;
import gov.nist.eee.output.ResultOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Result.Failure;
import gov.nist.eee.util.Result.Success;
import gov.nist.eee.util.Util;
import gov.nist.eee.util.function.QuadFunction;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.Stream;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;

@Pipeline(name = "quantity", internal = true)
@OutputMapper(ResultOutputMapper.class)
public class QuantityPipeline
        extends CellPipeline<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>
        implements IWithAssignableInputs {
    private static final Logger logger = LoggerFactory.getLogger(QuantityPipeline.class);

    /**
     * The tree path for BCN quantity values in the assignable input model.
     */
    public static final String QUANTITY_TREE_PATH = "bcnObjects.%d.quantity";

    /**
     * The tree path for BCN value per quantity in the assignable input model.
     */
    public static final String VALUES_TREE_PATH = "bcnObjects.%d.quantityValue";

    /**
     * The study period of the current request.
     */
    private Cell<CellSink<Integer>> cStudyPeriod;

    /**
     * The list of BCN IDs in the current request.
     */
    private Cell<List<Integer>> cIDs;

    /**
     * The list of Quantity Var Values in the current request associated with their BCN ID.
     */
    private Cell<Map<Integer, List<Double>>> cQuantityVarValue;
    private Cell<Map<Integer, VarRate>> cQuantityVarRate;
    private Cell<Map<Integer, CellSink<Double>>> cQuantity;
    private Cell<Map<Integer, CellSink<Integer>>> cInitialOccurrence;
    private Cell<Map<Integer, CellSink<Integer>>> cLife;
    private Cell<Map<Integer, CellSink<Integer>>> cEnd;
    private Cell<Map<Integer, CellSink<Integer>>> cInterval;
    private Cell<Map<Integer, Boolean>> cIsRecurring;

    @Override
    @SuppressWarnings("unchecked")
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up quantity pipeline");

        // Retrieve study period from analysis object
        var cAnalysis = sInput.map(Input::analysis);
        cStudyPeriod = cAnalysis.map(Analysis::studyPeriod).map(CellSink::new).hold(new CellSink<>(25));

        // Retrieve necessary values from BCN objects
        var cBcns = sInput.map(Input::bcnObjects).hold(List.of());

        cIDs = Util.toList(cBcns, Bcn::id);
        cQuantityVarValue = Util.toMap(cBcns, Bcn::id, Bcn::quantityVarValue);
        cQuantityVarRate = Util.toMap(cBcns, Bcn::id, Bcn::quantityVarRate);
        cQuantity = Util.toSinkMap(cBcns, Bcn::id, Bcn::quantity);
        cInitialOccurrence = Util.toSinkMap(cBcns, Bcn::id, Bcn::initialOccurrence);
        cLife = Cell.switchC(((Cell<Integer>) Cell.switchC((Cell) cStudyPeriod)).map(studyPeriod -> {
            return Util.toSinkMap(cBcns, Bcn::id, bcn -> bcn.life() == null ? studyPeriod : bcn.life());
        }));
        cEnd = Cell.switchC(((Cell<Integer>) Cell.switchC((Cell) cStudyPeriod)).map(studyPeriod ->
                Util.toSinkMap(cBcns, Bcn::id, bcn -> bcn.recur() == null || bcn.recur().end() == null ? studyPeriod : bcn.recur().end())
        ));
        cInterval = Util.toSinkMap(cBcns, Bcn::id, bcn -> bcn.recur() == null ? 1 : bcn.recur().interval());
        cIsRecurring = Util.toMap(cBcns, Bcn::id, bcn -> bcn.recur() != null);
    }

    @Override
    public Cell<Model> getAssignableInputs() {
        logger.trace("Creating assignable inputs for quantity pipeline");

        return Util.createInputModel(
                cQuantity.map(QuantityPipeline::addDoubleInputs),
                cInitialOccurrence.lift(cLife, cInterval, cEnd, cStudyPeriod, QuantityPipeline::addIntegerInputs)
        );
    }

    /**
     * Creates a function that adds all double inputs into the input tree.
     *
     * @param quantities a map of BCN IDs to their associated quantity cell sink.
     * @return a function that accepts a tree and adds the double inputs to that tree.
     */
    private static Consumer<Tree<String, CellSink<Double>>> addDoubleInputs(
            Map<Integer, CellSink<Double>> quantities
    ) {
        return doubleInputs -> {
            Util.addMapToTree(quantities, doubleInputs, QUANTITY_TREE_PATH);
        };
    }

    /**
     * Creates a function that adds all integer inputs into the input tree.
     *
     * @param initials  a map of BCN IDs to their associated initial recur cell sink.
     * @param lives     a map of BCN IDs to their associated lifetime cell sink.
     * @param ends      a map of BCN IDs to their associated recur end cell sink.
     * @param intervals a map of BCN IDs to their associated recur interval cell sink.
     * @return a function that accepts a tree and adds the integer inputs to that tree.
     */
    private static Consumer<Tree<String, CellSink<Integer>>> addIntegerInputs(
            Map<Integer, CellSink<Integer>> initials,
            Map<Integer, CellSink<Integer>> lives,
            Map<Integer, CellSink<Integer>> ends,
            Map<Integer, CellSink<Integer>> intervals,
            CellSink<Integer> studyPeriod
    ) {
        return integerInputs -> {
            integerInputs.add(new String[]{"analysisObject", "studyPeriod"}, studyPeriod);
            Util.addMapToTree(initials, integerInputs, "bcnObjects.%d.initialOccurrence");
            Util.addMapToTree(lives, integerInputs, "bcnObjects.%d.life");
            Util.addMapToTree(ends, integerInputs, "bcnObjects.%d.recur.end");
            Util.addMapToTree(intervals, integerInputs, "bcnObjects.%d.recur.interval");
        };
    }

    public static <A, B, C> BiFunction<A, CellSink<B>, Cell<C>> composeCell(BiFunction<A, B, C> func) {
        return (a, cell) -> cell.map(cellValue -> func.apply(a, cellValue));
    }

    public static <A, B, C, D, E> QuadFunction<Cell<A>, CellSink<B>, CellSink<C>, CellSink<D>, Cell<E>>
    composeCell(QuadFunction<A, B, C, D, E> func) {
        return (a, cell1, cell2, cell3) -> a.lift(cell1, cell2, cell3, func::apply);
    }

    public static <A, B, C, D, E> QuadFunction<CellSink<A>, CellSink<B>, CellSink<C>, Cell<D>, Cell<E>>
    composeCell2(QuadFunction<A, B, C, D, E> func) {
        return (a, cell1, cell2, cell3) -> a.lift(cell1, cell2, cell3, func::apply);
    }


    @Override
    public Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> define() {
        logger.trace("Defining quantity pipeline");

        var cMappedWithRateValues = getMappedValues(cEnd, cInitialOccurrence, cInterval, cQuantity, cQuantityVarRate, cQuantityVarValue, cStudyPeriod);

        var cEndPoint = cIDs.lift(cIsRecurring, cEnd, cInitialOccurrence, this::getEndPoints);

        var cInflatedValues = cQuantity.lift(
                (Cell<Integer>) Cell.switchC((Cell) cStudyPeriod), cInitialOccurrence, cInterval, cEndPoint,
                (quantities, studyPeriod, initials, intervals, ends) ->
                        Util.combineMap(quantities, initials, intervals, ends, composeCell2(getValueClosure(studyPeriod)))
        );

        var cShouldIncludes = cQuantityVarRate.lift(cQuantityVarValue, QuantityPipeline::shouldInflate);

        return cShouldIncludes.lift(cMappedWithRateValues, cInflatedValues, (shouldInclude, mapped, inflated) -> {
                    var result = new HashMap<Integer, Result<Cell<List<Double>>, E3Exception>>();
                    for (var entry : shouldInclude.entrySet()) {
                        var key = entry.getKey();
                        var value = entry.getValue();

                        result.put(key, value ? new Success<>(inflated.get(key)) : mapped.get(key));
                    }

                    return Util.resultSequence(result);
                }
        );
    }

    public static Cell<Map<Integer, Result<Cell<List<Double>>, E3Exception>>> getMappedValues(
            Cell<Map<Integer, CellSink<Integer>>> cEnd,
            Cell<Map<Integer, CellSink<Integer>>> cInitialOccurrence,
            Cell<Map<Integer, CellSink<Integer>>> cInterval,
            Cell<Map<Integer, CellSink<Double>>> cQuantity,
            Cell<Map<Integer, VarRate>> cQuantityVarRate,
            Cell<Map<Integer, List<Double>>> cQuantityVarValue,
            Cell<CellSink<Integer>> cStudyPeriod
    ) {
        var x1 = Cell.switchC(cQuantityVarValue
                        .lift(cStudyPeriod, (values, studyPeriod) -> {
                            return studyPeriod.map(s ->
                                    values.entrySet()
                                            .stream()
                                            .collect(Collectors.toMap(
                                                    Map.Entry::getKey,
                                                    e -> inflateVarValue(e.getValue(), s + 1)
                                            ))
                            );
                        })
                )
                .lift(cQuantityVarRate, QuantityPipeline::varRateMap);

        var x2 = x1.lift(cQuantity, (values, quantities) -> Util.combineMap(values, quantities, (value, quantity) -> {
            return value.map(v -> {
                return quantity.map(q -> Util.multiplier(v, q));
            });
        }));
        return x2.lift(cInitialOccurrence, cInterval, cEnd, (values, initials, intervals, ends) ->
                Util.combineMap(values, initials, intervals, ends, (valueResult, initial, interval, end) -> {
                    return valueResult.map(v -> {
                        return v.lift(initial, interval, end, QuantityPipeline::replaceOutside);
                    });
                }));
    }

    @NotNull
    private static QuadFunction<Double, Integer, Integer, Integer, List<Double>> getValueClosure(Integer studyPeriod) {
        return (quantity, initial, interval, end) -> getValues(studyPeriod, quantity, initial, interval, end);
    }

    @NotNull
    private static ArrayList<Double> getValues(Integer studyPeriod, Double quantity, Integer initial, Integer interval, Integer end) {
        var innerResult = new ArrayList<Double>(studyPeriod + 1);
        int validEnd = end == null || end == -1 ? studyPeriod : end;

        for (int i = 0; i < studyPeriod + 1; i++) {
            if (i >= initial && (i - initial) % interval == 0 && i <= validEnd)
                innerResult.add(quantity);
            else
                innerResult.add(0.0);
        }

        return innerResult;
    }

    /**
     * Get end points for all BCNs.
     *
     * @param ids
     * @param recurring
     * @param ends
     * @param initials
     * @return
     */
    private Map<Integer, Cell<Integer>> getEndPoints(
            List<Integer> ids,
            Map<Integer, Boolean> recurring,
            Map<Integer, CellSink<Integer>> ends,
            Map<Integer, CellSink<Integer>> initials
    ) {
        return Util.<Integer, Integer, Cell<Integer>>toMap(k -> k, id -> Cell.switchC(
                ends.get(id).lift(
                        initials.get(id),
                        (end, initial) -> getEndPoint(recurring.get(id), ends.get(id), initials.get(id), this.cStudyPeriod)
                )
        )).apply(ids);
    }

    /**
     * Determines where the end point for a cashflow should be given several
     *
     * @param recurring denotes whether the current BCN is recurring.
     * @param end       the end point that is defined from the BCN. Can be null.
     * @param initial   the initial timestep of the BCN.
     * @return the end point to use for calculations.
     */
    @SuppressWarnings("unchecked")
    public static Cell<Integer> getEndPoint(
            boolean recurring,
            @Nullable CellSink<Integer> end,
            CellSink<Integer> initial,
            Cell<CellSink<Integer>> cStudyPeriod
    ) {
        if (Boolean.TRUE.equals(recurring)) {
            if (end == null)
                return (Cell<Integer>) Cell.switchC((Cell) cStudyPeriod);

            return end;
        }

        return initial;
    }

    /**
     * Determines which BCNs need to be inflated before calculated quantities.
     *
     * @param rates  the map of {@link VarRate}s for each BCN.
     * @param values the map of Values for each BCN.
     * @return a map of booleans with true denoting that the corresponding BCN needs to be inflated. Otherwise, no
     * inflation is necessary.
     */
    public static Map<Integer, Boolean> shouldInflate(Map<Integer, VarRate> rates, Map<Integer, List<Double>> values) {
        return Util.combineMap(rates, values, (rate, value) -> rate == null || value == null);
    }

    /**
     * Maps all values with their corresponding var rates.
     *
     * @param values the values to map.
     * @param rates  the var rate to map with.
     * @return a map with BCN IDs corresponding to their mapped values.
     */
    public static Map<Integer, Result<List<Double>, E3Exception>> varRateMap(
            Map<Integer, Result<List<Double>, E3Exception>> values,
            Map<Integer, VarRate> rates
    ) {
        return Util.combineMap(values, rates,
                (result, rate) -> result.map(value -> QuantityPipeline.mapWithVarRate(value, rate))
        );
    }

    /**
     * Replaces any time steps in the given list outside the BCN occurrences with 0.
     *
     * @param values   The list of values to alter.
     * @param initial  The initial BCN occurrence time step.
     * @param interval The interval between BCN time steps.
     * @param end      The end of the BCN occurrences.
     * @return A new ArrayList containing only values inside the BCN occurrences. All values outside the BCN occurrences
     * will be 0.
     */
    public static List<Double> replaceOutside(List<Double> values, int initial, int interval, int end) {
        var result = new ArrayList<Double>(values.size());
        for (int i = 0; i < values.size(); i++) {
            result.add(isOutside(i, initial, interval, end) ? 0.0 : values.get(i));
        }

        return result;
    }

    /**
     * Checks if the given index is outside any BCN intervals, beginning, or end. Returns true if the index is outside
     * otherwise false. If any of the input values are negatives, false is also returned.
     *
     * @param index    The current time step to consider.
     * @param initial  The initial occurrence of the BCN.
     * @param interval The interval period for the BCN.
     * @param end      The end time step of the BCN.
     * @return True if the index is outside the BCN time frame, otherwise false. False is also returned if a parameter
     * is false.
     */
    public static boolean isOutside(int index, int initial, int interval, int end) {
        return isBeforeInitial(index, initial) || isNotInInterval(index, initial, interval) || isAfterEnd(index, end);
    }

    /**
     * Checks if the given index is before the initial BCN occurrence. Returns true if the index is before the initial
     * otherwise false.
     *
     * @param index   The time step to check.
     * @param initial The initial BCN occurrence to check against.
     * @return True if the index is before the initial otherwise false. False is also returned if nay of the parameters
     * are negative.
     */
    public static boolean isBeforeInitial(int index, int initial) {
        if (index < 0 || initial < 0)
            return false;

        return index < initial;
    }

    /**
     * Checks if the given index it outside the given interval. For example, if the interval is every two time steps
     * then if index is 3 then this method will return true since 3 is not a multiple of 2. This can also be aligned
     * to a given initial starting time step.
     * <p>
     * Negative values are not permitted and will return false.
     *
     * @param index    The current time step to consider.
     * @param initial  The beginning of the BCN life. Used to align interval calculation.
     * @param interval The number of time steps between each BCN occurrence.
     * @return True if the given index is outside any BCN interval occurrences, otherwise false. False is returned if
     * any of the parameters are negative.
     */
    public static boolean isNotInInterval(int index, int initial, int interval) {
        if (interval <= 0 || index < 0 || initial < 0)
            return false;

        return (index - initial) % interval != 0;
    }

    /**
     * Checks if the given index and end indicate that a BCN is after the BCN life ends;
     *
     * @param index The current index of the calculation.
     * @param end   The end time step of the BCN.
     * @return True if the given index is after the end point, otherwise false. Negative values are not permitted
     * and false will be returned if either parameter is negative.
     */
    public static boolean isAfterEnd(int index, int end) {
        if (index < 0 || end < 0)
            return false;

        return index > end;
    }

    /**
     * Maps input values by the formula corresponding to the given VarRate. For Year By Year the values are not
     * altered, for Percent Delta the values are compounded throughout the study period.
     *
     * @param values              The values to iterate.
     * @param varRate             The Var Rate to determine how to map the values.
     * @param compoundingFunction The function that should be applied when the var rate is set to
     *                            {@link VarRate#PERCENT_DELTA}.
     * @return Either the unaltered values or the values compounded over time.
     */
    public static List<Double> mapWithVarRate(
            List<Double> values,
            VarRate varRate,
            Function<List<Double>, List<Double>> compoundingFunction
    ) {
        if (values == null || varRate == null)
            return List.of();

        return switch (varRate) {
            case YEAR_BY_YEAR -> values;
            case PERCENT_DELTA -> compoundingFunction.apply(values);
        };
    }

    /**
     * Maps input values by the formula corresponding to the given {@link VarRate}. For {@link VarRate#YEAR_BY_YEAR}
     * the values are not altered, for {@link VarRate#PERCENT_DELTA} the values are compounded throughout the study
     * period. Defaults to using {@link Util#compound(List)} for the {@link VarRate#PERCENT_DELTA} case.
     *
     * @param values  The values to iterate.
     * @param varRate The Var Rate to determine how to map the values.
     * @return Either the unaltered values or the values compounded over time.
     */
    public static List<Double> mapWithVarRate(List<Double> values, VarRate varRate) {
        return mapWithVarRate(values, varRate, Util::compound);
    }

    /**
     * Inflate the given var value list into a list of the given size. This normalizes lists of single values and lists
     * of the exact size value into lists that have the correct length of the given size value.
     *
     * @param varValue The var value retrieved from the BCN. Must be equal to the size, or must only have one element.
     * @param size     The size the return list should be.
     * @return A list with the inflated values.
     */
    public static Result<List<Double>, E3Exception> inflateVarValue(List<Double> varValue, int size) {
        // Size cannot be less than zero.
        if (size <= 0) {
            return new Failure<>(new E3Exception(
                    ErrorCode.E7102_INFLATE_LESS_THAN_ONE,
                    String.format("Tried to inflate var values %1$s into a list with size %2$d", varValue, size)
            ));
        }

        // VarValue cannot be null
        if (varValue == null)
            return new Failure<>(new E3Exception(ErrorCode.E7103_VAR_VALUE_NULL));

        // If the var value array is the same size as the given size, return it.
        if (varValue.size() == size)
            return new Success<>(varValue);

        // Any var value size other than  1 are disallowed.
        if (varValue.size() != 1) {
            return new Failure<>(new E3Exception(
                    ErrorCode.E7104_PARTIALLY_DEFINED_VAR_VALUE,
                    String.format("Given: %1$s", varValue)
            ));
        }

        // Create a new list which is the same size as the given size value and copy the single var value element into
        // the new list.
        var result = new ArrayList<Double>(size);
        var value = varValue.get(0);

        result.add(0.0);
        for (int i = 1; i < size; i++) {
            result.add(value);
        }

        return new Success<>(result);
    }
}
