package gov.nist.eee.pipeline.sensitivity;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.output.ResultListMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.discounted.DiscountedPipeline;
import gov.nist.eee.pipeline.measures.MeasureSummary;
import gov.nist.eee.pipeline.measures.MeasureSummaryPipeline;
import gov.nist.eee.pipeline.sensitivity.input.Sensitivity;
import gov.nist.eee.pipeline.sensitivity.input.SensitivityDiffType;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

import static gov.nist.eee.pipeline.sensitivity.SensitivityErrorCode.E0002_NO_VARIABLE_IN_TREE;

@Pipeline(name = "sensitivity", dependencies = {MeasureSummaryPipeline.class}, inputDependencies = {DiscountedPipeline.class})
@OutputMapper(ResultListMapper.class)
public class SensitivityPipeline
        extends CellPipeline<Result<List<SensitivitySummary>, E3Exception>>
        implements IWithDependency, IWithInput {
    private static final Logger logger = LoggerFactory.getLogger(SensitivityPipeline.class);
    public static final String TREE_PATTERN = "[.\\[\\]]+";

    /**
     * Contains a list of all the requested sensitivity analyses from the extension input.
     */
    private Cell<List<Sensitivity>> cSensitivityObjects;

    private Cell<Map<Integer, Result<CellSink<Double>, E3Exception>>> cSinkCells;

    private Cell<Result<Map<Integer, Cell<List<MeasureSummary>>>, E3Exception>> cGroupedMeasureSummaries;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up sensitivity pipeline");
        cSensitivityObjects = sInput.map(Input::extensions).map(this::sensitivityFromInput).hold(List.of());
    }

    @SuppressWarnings("unchecked")
    private List<Sensitivity> sensitivityFromInput(final Map<String, Object> extensions) {
        return (List<Sensitivity>) extensions.getOrDefault("sensitivityObjects", List.of());
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for sensitivity pipeline. " + parameters);

        Cell<Result<Map<Integer, Cell<MeasureSummary>>, E3Exception>> cMeasureSummaries = parameters.get(MeasureSummaryPipeline.class);
        cGroupedMeasureSummaries = cMeasureSummaries.lift(cSensitivityObjects, (measureSummaries, sensitivities) -> measureSummaries.map(measures -> {
            var result = new HashMap<Integer, Cell<List<MeasureSummary>>>();
            for (var sensitivity : sensitivities) {
                var sensitivityMeasures = sensitivity.altIds().stream().map(measures::get).toList();
                result.put(sensitivity.id(), CellUtils.sequence(sensitivityMeasures));
            }
            return result;
        }));
    }

    @Override
    public void setupInput(Cell<Model> cModel) {
        logger.debug("Setup input for sensitivity pipeline");

        this.cSinkCells = cSensitivityObjects.lift(
                cModel,
                (sensitivities, model) ->
                        sensitivities.stream()
                                .collect(Collectors.toMap(Sensitivity::id, s ->
                                                getModelCell(s.variable().split(TREE_PATTERN), model)
                                        )
                                )
        );
    }

    public Result<CellSink<Double>, E3Exception> getModelCell(String[] path, Model model) {
        // Try to get double value from tree
        try {
            return new Result.Success<>(model.doubleInputs().get(path));
        } catch (IllegalArgumentException e) {
            logger.debug(e.toString());
        }

        // If there is no double in the tree, try to get an integer.
        try {
            var intCell = model.intInputs().get(path);
            var doubleCell = new CellSink<>((double) intCell.sample());
            doubleCell.listen(d -> Transaction.post(() -> intCell.send(d.intValue())));
            return new Result.Success<>(doubleCell);
        } catch (IllegalArgumentException e) {
            logger.error(e.toString());
        }

        // If neither a double nor integer value is in the tree for the requested variable, return a failure.
        return new Result.Failure<>(new E3Exception(E0002_NO_VARIABLE_IN_TREE));
    }

    @Override
    public Cell<Result<List<SensitivitySummary>, E3Exception>> define() {
        logger.trace("Defining sensitivity pipeline");

        return cSensitivityObjects.lift(cSinkCells, cGroupedMeasureSummaries, this::mapSensitivities);
    }

    private Result<List<SensitivitySummary>, E3Exception> mapSensitivities(
            List<Sensitivity> sensitivities,
            Map<Integer, Result<CellSink<Double>, E3Exception>> sinkCells,
            Result<Map<Integer, Cell<List<MeasureSummary>>>, E3Exception> groupedSummaries
    ) {
        return Util.resultSequence(
                sensitivities.stream()
                        .map(sensitivity -> runSensitivity(sinkCells, groupedSummaries, sensitivity))
                        .filter(Objects::nonNull)
                        .toList()
        );
    }

    private Result<SensitivitySummary, E3Exception> runSensitivity(
            Map<Integer, Result<CellSink<Double>, E3Exception>> sinkCells,
            Result<Map<Integer, Cell<List<MeasureSummary>>>, E3Exception> groupedSummaries,
            Sensitivity sensitivity
    ) {
        var rSink = sinkCells.get(sensitivity.id());

        return rSink.flatMap(sink -> groupedSummaries.map(grouped -> {
            var original = sink.sample();
            var list = getValues(sensitivity.diffType(), original, sensitivity.diffValue());
            var accumulator = new HashMap<Integer, List<MeasureSummary>>();

            for (var i : list) {
                var measure = recalculate(i, sink, grouped.get(sensitivity.id()));

                addMeasuresToMap(accumulator, measure);
            }

            return new SensitivitySummary(sensitivity.id(), accumulator);
        }));
    }

    private static void addMeasuresToMap(
            HashMap<Integer, List<MeasureSummary>> accumulator,
            List<MeasureSummary> measures
    ) {
        for (var measure : measures) {
            var mAltID = measure.altId();
            var resultList = accumulator.computeIfAbsent(mAltID, ArrayList::new);
            resultList.add(measure);
        }
    }

    private static Lambda2<List<MeasureSummary>, HashMap<Integer, List<MeasureSummary>>, HashMap<Integer, List<MeasureSummary>>> createAccumulator(int id) {
        return (value, m) -> {
            var l = m.computeIfAbsent(id, ArrayList::new);
            l.addAll(value);
            return m;
        };
    }

    private List<MeasureSummary> recalculate(
            final double x,
            final CellSink<Double> sink,
            final Cell<List<MeasureSummary>> cMeasureSummary
    ) {
        Transaction.post(() -> sink.send(x));
        return cMeasureSummary.sample();
    }

    public static List<Double> getValues(SensitivityDiffType diffType, Number original, double diffValue) {
        return switch (diffType) {
            case GROSS, POSITIVE_GROSS, NEGATIVE_GROSS -> getValuesGross(diffType, original, diffValue);
            case PERCENT, POSITIVE_PERCENT, NEGATIVE_PERCENT -> getValuesPercent(diffType, original, diffValue);
        };
    }

    public static List<Double> getValuesGross(SensitivityDiffType diffType, Number original, double diffValue) {
        var result = new ArrayList<Double>();

        if (diffType == SensitivityDiffType.GROSS || diffType == SensitivityDiffType.POSITIVE_GROSS)
            result.add((Double) getUpperGross(original, diffValue));

        if (diffType == SensitivityDiffType.GROSS || diffType == SensitivityDiffType.NEGATIVE_GROSS)
            result.add((Double) getLowerGross(original, diffValue));

        result.add((Double) original);

        return result;
    }

    public static List<Double> getValuesPercent(SensitivityDiffType diffType, Number original, double diffValue) {
        var result = new ArrayList<Double>();

        if (diffType == SensitivityDiffType.PERCENT || diffType == SensitivityDiffType.POSITIVE_PERCENT)
            result.add((Double) getUpperPercent(original, diffValue));

        if (diffType == SensitivityDiffType.PERCENT || diffType == SensitivityDiffType.NEGATIVE_PERCENT)
            result.add((Double) getLowerPercent(original, diffValue));

        result.add((Double) original);

        return result;
    }

    public static Number getUpperPercent(Number original, double diffValue) {
        if (original instanceof Double originalDouble) return originalDouble * (1.0 + diffValue);
        else if (original instanceof Integer originalInteger) return originalInteger * (1 + (int) diffValue);

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }

    public static Number getLowerPercent(Number original, double diffValue) {
        if (original instanceof Double originalDouble) return originalDouble * (1.0 - diffValue);
        else if (original instanceof Integer originalInteger) return originalInteger * (1 - (int) diffValue);

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }

    public static Number getUpperGross(Number original, double diffValue) {
        if (original instanceof Double originalDouble) return originalDouble + diffValue;
        else if (original instanceof Integer originalInteger) return originalInteger + (int) diffValue;

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }

    public static Number getLowerGross(Number original, double diffValue) {
        if (original instanceof Double originalDouble) return originalDouble - diffValue;
        else if (original instanceof Integer originalInteger) return originalInteger - (int) diffValue;

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }
}
