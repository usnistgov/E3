package gov.nist.eee.pipeline.residualvalue;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Bcn;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.output.ResultOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.pipeline.value.ValuePipeline;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Pipeline(name = "residualvalue", dependencies = {ValuePipeline.class}, inputDependencies = {QuantityPipeline.class})
@OutputMapper(ResultOutputMapper.class)
public class ResidualValuePipeline
        extends CellPipeline<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>
        implements IWithDependency, IWithInput {
    private static final Logger logger = LoggerFactory.getLogger(ResidualValuePipeline.class);
    private Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> cValues;
    private Cell<Integer> cStudyPeriod;
    private Cell<Result<Map<Integer, Cell<Integer>>, E3Exception>> cLife;
    private Cell<Result<Map<Integer, Cell<Integer>>, E3Exception>> cEnd;
    private Cell<Result<Map<Integer, Cell<Integer>>, E3Exception>> cInterval;
    private Cell<Map<Integer, ResidualValueVariables>> cResidualValueVariables;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up residual value pipeline.");

        var cBcns = sInput.map(Input::bcnObjects).hold(List.of());
        cResidualValueVariables = Util.toMap(cBcns, Bcn::id, bcn -> new ResidualValueVariables(
                bcn.initialOccurrence(), bcn.recur() == null, bcn.residualValue(), bcn.residualValueOnly()
        ));
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for residual value pipeline");

        cValues = parameters.get(ValuePipeline.class);
    }

    @Override
    public void setupInput(Cell<Model> cModel) {
        logger.trace("Setting up inputs for residual value pipeline");

        cStudyPeriod = Cell.switchC(cModel.map(model ->
                model.intInputs().get(new String[]{"analysisObject", "studyPeriod"})
        ));

        cLife = cModel.lift(cValues, (model, values) -> values.map(v -> {
            var result = new HashMap<Integer, Cell<Integer>>();
            for (var id : v.keySet()) {
                result.put(id, model.intInputs().get(new String[]{"bcnObjects", id.toString(), "life"}));
            }
            return result;
        }));

        cInterval = cModel.lift(cValues, (model, values) -> values.map(v -> {
            var result = new HashMap<Integer, Cell<Integer>>();
            for (var id : v.keySet()) {
                result.put(id, model.intInputs().get(new String[]{"bcnObjects", id.toString(), "recur", "interval"}));
            }
            return result;
        }));

        cEnd = cModel.lift(cValues, (model, values) -> values.map(v -> {
            var result = new HashMap<Integer, Cell<Integer>>();
            for (var id : v.keySet()) {
                result.put(id, model.intInputs().get(new String[]{"bcnObjects", id.toString(), "recur", "end"}));
            }
            return result;
        }));
    }

    @Override
    public Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> define() {
        logger.trace("Defining residual value pipeline");

        return cValues.lift(
                cStudyPeriod,
                cResidualValueVariables,
                cLife,
                cEnd,
                cInterval,
                (values, studyPeriod, bcnVariables, life, end, interval) -> {
                    return values.flatMap(v -> {
                        return life.flatMap(l -> {
                            return end.flatMap(e -> {
                                return interval.map(i -> {
                                    var result = new HashMap<Integer, Cell<List<Double>>>();

                                    for (var entry : v.entrySet()) {
                                        var key = entry.getKey();
                                        var value = entry.getValue();
                                        var variables = bcnVariables.get(key);

                                        if (!variables.hasResidualValue()) {
                                            result.put(key, value);
                                            continue;
                                        }

                                        if (variables.hasResidualValueOnly()) {
                                            result.put(key, residualValueOnly(value, variables.initial()));
                                            continue;
                                        }

                                        result.put(key, combineResidualValue(
                                                value,
                                                studyPeriod,
                                                l.get(key),
                                                variables.initial(),
                                                e.get(key),
                                                i.get(key),
                                                variables.isRecurNull()
                                        ));
                                    }

                                    return result;

                                });
                            });
                        });

                    });
                }
        );
    }

    private Cell<List<Double>> combineResidualValue(
            Cell<List<Double>> cValues,
            int studyPeriod,
            Cell<Integer> cLife,
            int initial,
            Cell<Integer> cEnd,
            Cell<Integer> cInterval,
            boolean isRecurNull
    ) {
        return residualValue(cValues, studyPeriod, cLife, initial, cEnd, cInterval, isRecurNull).lift(
                cValues,
                (residualValue, values) -> {
                    var result = new ArrayList<Double>(studyPeriod + 1);
                    result.addAll(values);
                    result.set(result.size() - 1, result.get(result.size() - 1) + residualValue);
                    return result;
                }
        );
    }

    private Cell<Double> residualValue(
            Cell<List<Double>> cValues,
            int studyPeriod,
            Cell<Integer> cLife,
            int initial,
            Cell<Integer> cEnd,
            Cell<Integer> cInterval,
            boolean isRecurNull
    ) {
        var cRemainingLife = remainingLife(studyPeriod, cLife, initial, cEnd, cInterval, isRecurNull);
        return cValues.lift(cLife, cRemainingLife, (values, life, remainingLife) ->
                calculateResidualValue(remainingLife, life, initial, values)
        );
    }

    private Cell<List<Double>> residualValueOnly(Cell<List<Double>> cValues, int initial) {
        return cValues.map(values -> {
            var result = new ArrayList<Double>(values.size());

            for (int i = 0; i < values.size() - 1; i++) {
                result.add(0.0);
            }
            result.add(-values.get(initial));

            return result;
        });
    }

    /**
     * Calculates the monetary value for the residual value of a BCN.
     *
     * @param remaining the remaining life for the BCN.
     * @param life      the lifetime of the BCN.
     * @param initial   the initial occurrence or the BCN.
     * @param values    a list of value for the BCN.
     * @return the monetary value of the remaining life of the BCN.
     */
    public static double calculateResidualValue(double remaining, int life, int initial, List<Double> values) {
        return (-remaining / life) * values.get(initial);
    }

    private Cell<Double> remainingLife(
            int studyPeriod,
            Cell<Integer> cLife,
            int initial,
            Cell<Integer> cEnd,
            Cell<Integer> cInterval,
            boolean isRecurNull
    ) {
        return cLife.lift(cEnd, cInterval, (life, end, interval) -> {
                    if (isRecurNull)
                        return remainingLifeNonRecurring(studyPeriod, life, initial);

                    return remainingLifeRecurring(studyPeriod, end, life, initial, interval);
                }
        );
    }

    /**
     * @param studyPeriod
     * @param life
     * @param initial
     * @return
     */
    public static double remainingLifeNonRecurring(int studyPeriod, int life, int initial) {
        var result = life - studyPeriod;

        if (initial != 0)
            result += initial - 1;

        return result;
    }

    /**
     * Returns the amount of life remaining after the study period for a BCN if it is recurring.
     *
     * @param studyPeriod
     * @param end
     * @param life
     * @param initial
     * @param interval
     * @return
     */
    public static double remainingLifeRecurring(int studyPeriod, int end, int life, int initial, int interval) {
        if (endDateWithinPeriod(studyPeriod, end) || lifetimeWithinPeriod(studyPeriod, life, initial, interval))
            return 0.0;

        return life - (studyPeriod - initial - lastInterval(studyPeriod, initial, interval));
    }

    /**
     * Returns true if the given end point is less than or equal to the study period, otherwise return false.
     *
     * @param studyPeriod the length of the study period.
     * @param end         the endpoint of the BCN.
     * @return true if end is less than or equal to the study period, otherwise false.
     */
    public static boolean endDateWithinPeriod(int studyPeriod, int end) {
        return end <= studyPeriod;
    }

    /**
     * Returns true if the lifetime of a BCN is within the study period.
     *
     * @param studyPeriod the length of the analysis study period
     * @param life        the lifetime of the BCN
     * @param initial     the first occurrence of the BCN
     * @param interval    the number of time steps between BCN recurrences.
     * @return true if the lifetime of the BCN in its last occurrence is within the study period, otherwise false
     */
    public static boolean lifetimeWithinPeriod(int studyPeriod, int life, int initial, int interval) {
        return studyPeriod >= life + lastInterval(studyPeriod, initial, interval) - 1;
    }

    /**
     * Returns the last timestep before the end of the study period that a BCN occurs on.
     *
     * @param studyPeriod the length of the analysis study period
     * @param initial     the first occurrence of the BCN
     * @param interval    the number of time steps between BCN recurrences.
     * @return the last timestep before the end of the study period.
     */
    public static double lastInterval(double studyPeriod, double initial, double interval) {
        // If there is no interval, then only the initial occurrence happens.
        if (interval == 0)
            return initial;

        return Math.floor((studyPeriod - initial) / interval) * interval + initial;
    }
}
