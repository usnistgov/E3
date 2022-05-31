package gov.nist.e3.compute;

import gov.nist.e3.objects.input.RecurOptions;
import gov.nist.e3.objects.input.VarRate;
import gov.nist.e3.util.Util;
import nz.sodium.Cell;
import nz.sodium.Transaction;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class QuantityPipeline {
    private static final Logger log = LoggerFactory.getLogger(QuantityPipeline.class);

    public final Cell<List<Double>> cQuantities;

    public QuantityPipeline(
            @NotNull Cell<Double> cQuantity,
            @NotNull List<Double> varValue,
            @NotNull VarRate varRate,
            @NotNull Cell<Integer> cInitialOccurrence,
            Cell<Integer> cIntervalOrNull,
            Cell<Integer> cEndOrNull,
            @NotNull Cell<Integer> cStudyPeriod,
            @Nullable RecurOptions recur
    ) {
        var cInterval = cIntervalOrNull == null ? new Cell<>(1) : cIntervalOrNull;
        var cEnd = cEndOrNull.lift( //TODO: remove this since end is a primitive?
                cStudyPeriod,
                (endOrNull, studyPeriod) -> {
                    if (endOrNull == null)
                        return studyPeriod;

                    return endOrNull;
                }
        );

        this.cQuantities = define(cQuantity, varValue, varRate, cInitialOccurrence, cInterval, cEnd, cStudyPeriod, recur);
    }

    /**
     * Defines a data flow that computes the quantity values for the given input.
     *
     * @return a cell that contains a list of doubles that represents the quantity values for the input.
     */
    public Cell<List<Double>> define(
            @NotNull Cell<Double> cQuantity,
            @Nullable List<Double> varValue,
            @Nullable VarRate varRate,
            @NotNull Cell<Integer> cInitialOccurrence,
            @NotNull Cell<Integer> cInterval,
            @NotNull Cell<Integer> cEnd,
            @NotNull Cell<Integer> cStudyPeriod,
            @Nullable RecurOptions recur
    ) {
        return Transaction.run(() -> {
            var includeVarRateMap = Util.nonNull(varValue, varRate);

            if (includeVarRateMap) {
                var cInflatedOrDefault = inflatedOrDefault(varValue, cStudyPeriod);

                return cInflatedOrDefault.map(values -> Util.mapWithVarRate(values, varRate))
                        .lift(cQuantity, Util::multiplier)
                        .lift(cInitialOccurrence, cInterval, cEnd, QuantityPipeline::replaceOutside);
            } else {
                var isRecurring = Util.nonNull(recur);

                return cQuantity.lift(
                        cStudyPeriod,
                        cInitialOccurrence,
                        cInterval,
                        cEnd,
                        (quantity, studyPeriod, initialOccurrence, interval, endOrInvalid) -> {
                            var result = new ArrayList<Double>(studyPeriod + 1);
                            var end = isRecurring ? endOrInvalid == -1 ? studyPeriod : endOrInvalid : initialOccurrence;

                            for (int i = 0; i < studyPeriod + 1; i++) {
                                if (i >= initialOccurrence && (i - initialOccurrence) % interval == 0 && i <= end)
                                    result.add(quantity);
                                else
                                    result.add(0.0);
                            }

                            return result;
                        }).lift(cInitialOccurrence, cInterval, cEnd, QuantityPipeline::replaceOutside);
            }
        });
    }

    public static Cell<List<Double>> inflatedOrDefault(List<Double> varValue, Cell<Integer> cStudyPeriod) {
        // Inflate var values if necessary otherwise just return cell with var values.
        if(varValue.size() == 1)
            return cStudyPeriod.map(studyPeriod -> Util.inflateVarValue(varValue, studyPeriod + 1));
        else
            return new Cell<>(varValue);
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
        if (interval == 0 || index < 0 || initial < 0)
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
}
