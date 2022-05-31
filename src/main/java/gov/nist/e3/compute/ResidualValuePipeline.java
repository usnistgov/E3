package gov.nist.e3.compute;

import gov.nist.e3.objects.input.RecurOptions;
import nz.sodium.Cell;
import nz.sodium.Transaction;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class ResidualValuePipeline {
    private static final Logger log = LoggerFactory.getLogger(QuantityPipeline.class);

    public final Cell<List<Double>> cValuesWithResidual;

    public ResidualValuePipeline(
            Cell<List<Double>> cValues,
            Cell<Integer> cStudyPeriod,
            Cell<Integer> cLife,
            Cell<Integer> cInitial,
            @Nullable RecurOptions recurOptions,
            boolean residualValue,
            boolean residualValueOnly
    ) {
        this.cValuesWithResidual = this.define(cValues, cStudyPeriod, cLife, cInitial, recurOptions, residualValue, residualValueOnly);
    }

    private Cell<List<Double>> define(
            Cell<List<Double>> cValues,
            Cell<Integer> cStudyPeriod,
            Cell<Integer> cLife,
            Cell<Integer> cInitial,
            @Nullable RecurOptions recurOptions,
            boolean residualValue,
            boolean residualValueOnly
    ) {
        return Transaction.run(() -> {
            if (!residualValue)
                return cValues;

            if (residualValueOnly)
                return residualValueOnly(cValues, cInitial);
            else
                return combineResidualValue(cValues, cStudyPeriod, cLife, cInitial, recurOptions);
        });
    }

    private Cell<List<Double>> residualValueOnly(
            Cell<List<Double>> cValues,
            Cell<Integer> cInitial
    ) {
        return cValues.lift(cInitial, (values, initial) -> {
            var result = new ArrayList<Double>(values.size());

            for (int i = 0; i < values.size() - 1; i++) {
                result.add(0.0);
            }
            result.add(-values.get(initial));

            return result;
        });
    }

    private Cell<List<Double>> combineResidualValue(
            Cell<List<Double>> cValues,
            Cell<Integer> cStudyPeriod,
            Cell<Integer> cLife,
            Cell<Integer> cInitial,
            @Nullable RecurOptions recurOptions
    ) {
        return residualValue(cValues, cStudyPeriod, cLife, cInitial, recurOptions).lift(
                cValues,
                cStudyPeriod,
                (residualValue, values, studyPeriod) -> {
                    var result = new ArrayList<Double>(studyPeriod + 1);
                    result.addAll(values);
                    result.set(result.size() - 1, result.get(result.size() - 1) + residualValue);
                    return result;
                }
        );
    }

    private Cell<Double> residualValue(
            Cell<List<Double>> cValues,
            Cell<Integer> cStudyPeriod,
            Cell<Integer> cLife,
            Cell<Integer> cInitial,
            @Nullable RecurOptions recurOptions
    ) {
        var cRemainingLife = cStudyPeriod.lift(
                cLife,
                cInitial,
                (studyPeriod, life, initial) -> remainingLife(studyPeriod, life, initial, recurOptions)
        );

        return cRemainingLife.lift(cLife, cInitial, cValues, this::calculateResidualValue);
    }

    private double calculateResidualValue(double remaining, int life, int initial, List<Double> values) {
        return (-remaining / life) * values.get(initial);
    }

    private double remainingLife(
            int studyPeriod,
            int life,
            int initial,
            @Nullable RecurOptions recurOptions
    ) {
        var end = recurOptions == null ? studyPeriod : recurOptions.end();
        var interval = recurOptions == null ? 1 : recurOptions.interval();

        if (recurOptions != null && (endDateWithinPeriod(studyPeriod, end) || lifetimeWithinPeriod(studyPeriod, life, initial, interval)))
            return 0;
        else if (recurOptions != null)
            return life - (studyPeriod - initial - lastInterval(studyPeriod, initial, recurOptions.interval()));
        else
            return life - (studyPeriod - initial);
    }

    private boolean endDateWithinPeriod(int studyPeriod, int end) {
        return end <= studyPeriod;
    }

    private boolean lifetimeWithinPeriod(int studyPeriod, int life, int initial, int interval) {
        return studyPeriod >= life + lastInterval(studyPeriod, initial, interval) - 1;
    }

    private double lastInterval(double studyPeriod, double initial, double interval) {
        return Math.floor((studyPeriod - initial) / interval) * interval + initial;
    }
}
