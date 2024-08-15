package gov.nist.eee.pipeline.uncertainty;

import gov.nist.eee.config.Config;
import gov.nist.eee.error.E3Exception;
import gov.nist.eee.error.ErrorCode;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Alternative;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.output.ResultListMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.measures.MeasureSummary;
import gov.nist.eee.pipeline.measures.MeasureSummaryPipeline;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.pipeline.uncertainty.input.Uncertainty;
import gov.nist.eee.pipeline.uncertainty.input.UncertaintyVariable;
import gov.nist.eee.pipeline.uncertainty.output.UncertaintyMeasureSummary;
import gov.nist.eee.pipeline.value.ValuePipeline;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.*;
import org.apache.commons.math3.random.JDKRandomGenerator;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

import static gov.nist.eee.pipeline.uncertainty.UncertaintyErrorCode.E0003_NO_VARIABLE_IN_TREE;

@Pipeline(name = "uncertainty", dependencies = MeasureSummaryPipeline.class, inputDependencies = {QuantityPipeline.class, ValuePipeline.class})
@OutputMapper(ResultListMapper.class)
public class UncertaintyPipeline
        extends SynchronousPipeline<Result<List<Map<Integer, UncertaintyMeasureSummary>>, E3Exception>>
        implements IWithDependency, IWithInput {
    private static final Logger logger = LoggerFactory.getLogger(UncertaintyPipeline.class);
    public static final String TREE_PATTERN = "[.\\[\\]]+";

    private Cell<List<Uncertainty>> cUncertaintyObjects;
    private Cell<Map<Integer, Result<List<CellSink<Double>>, E3Exception>>> cSinkCells;
    private Cell<Map<Integer, Set<Integer>>> cBcnAltIDs;
    private Cell<List<Integer>> cAltIDs;
    private Cell<Model> cModel;
    private Cell<Result<Map<Integer, Cell<MeasureSummary>>, E3Exception>> cMeasureSummaries;
    private final Cell<UncertaintyConfig> cConfig = Config.cConfigs.map(config -> {
        var uncertaintyConfig = (Map<String, Object>) config.get("uncertainty");
        return new UncertaintyConfig(
                (int) uncertaintyConfig.getOrDefault("maxIterations", 10000),
                (int) uncertaintyConfig.getOrDefault("minIterations", 1000),
                (int) uncertaintyConfig.getOrDefault("stride", 500),
                (double) uncertaintyConfig.getOrDefault("tolerance", 0.001)
        );
    });

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up uncertainty pipeline");
        cUncertaintyObjects = sInput.map(Input::extensions).map(this::getUncertaintyFromInput).hold(List.of());

        cBcnAltIDs = sInput.map(Input::alternativeObjects).hold(List.of()).map(Util::groupByBcn);
        cAltIDs = sInput.map(Input::alternativeObjects)
                .hold(List.of())
                .map(alts -> alts.stream().map(Alternative::id).toList());
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for sensitivity pipeline. " + parameters);

        cMeasureSummaries = parameters.get(MeasureSummaryPipeline.class);
    }

    @Override
    public void setupInput(Cell<Model> cModel) {
        logger.debug("Setup input for sensitivity pipeline");
        this.cModel = cModel;
    }

    @Override
    public Result<List<Map<Integer, UncertaintyMeasureSummary>>, E3Exception> run() {
        logger.debug("Running synchronous run method of uncertainty pipeline");

        var config = cConfig.sample();

        return cMeasureSummaries.sample().map(measureSummaries -> {
            var result = new ArrayList<Map<Integer, UncertaintyMeasureSummary>>();

            var model = cModel.sample();
            var uncertainties = cUncertaintyObjects.sample();
            var bcnAltIDs = cBcnAltIDs.sample();
            var altIDs = cAltIDs.sample();

            for (var uncertainty : uncertainties) {
                var rng = getRNG(uncertainty.seed());
                var distributionActions = getUncertaintyActions(uncertainty.variables(), rng, model);
                var affectedAlternatives = getAffectedAlternatives(uncertainty.variables(), bcnAltIDs, altIDs);

                var summaries = measureSummaries.entrySet()
                        .stream()
                        .filter(entry -> affectedAlternatives.contains(entry.getKey()))
                        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

                var stopConditions = summaries.values()
                        .stream()
                        .flatMap(summary -> java.util.stream.Stream.of(
                                createMeasureStopCondition(summary, MeasureSummary::totalCosts, config.tolerance()),
                                createMeasureStopCondition(summary, MeasureSummary::totalBenefits, config.tolerance()),
                                createMeasureStopCondition(summary, MeasureSummary::totalCostsInvest, config.tolerance()),
                                createMeasureStopCondition(summary, MeasureSummary::totalCostNonInvest, config.tolerance())
                        ))
                        .toList();

                var builders = summaries.entrySet()
                        .stream()
                        .map(entry -> new UncertaintySummaryBuilder(uncertainty.id(), entry.getKey())
                                .bindMeasureSummary(entry.getValue())
                        )
                        .toList();

                run(
                        config.maxIterations(),
                        stopConditions,
                        distributionActions,
                        config.minIterations(),
                        config.stride()
                );

                result.add(
                        builders.stream().collect(
                                Collectors.toMap(UncertaintySummaryBuilder::getAltID, UncertaintySummaryBuilder::build)
                        )
                );
            }

            return result;
        });
    }

    private void run(int max, List<StopCondition> stopConditions, List<Runnable> actions, int min, int stride) {
        int i = 0;

        while (i < max) {
            logger.debug("iteration {}", i);

            if (shouldStop(stopConditions, i, min, stride))
                break;

            runTransactions(actions);
            stopConditions.forEach(StopCondition::update);

            i++;
        }
    }

    private static boolean shouldStop(List<StopCondition> stopConditions, int iteration, int minIterations, int stride) {
        return iteration >= minIterations && iteration % stride == 0 && stopConditions.stream().allMatch(StopCondition::shouldStop);
    }

    private void runTransactions(List<Runnable> distributionActions) {
        Transaction.runVoid(() -> distributionActions.forEach(Runnable::run));
    }

    private StopCondition createMeasureStopCondition(Cell<MeasureSummary> summary, Lambda1<MeasureSummary, Double> getter, double tolerance) {
        return new StopCondition(summary.map(getter), tolerance);
    }

    private List<Runnable> getUncertaintyActions(
            List<UncertaintyVariable> variables,
            JDKRandomGenerator rng,
            Model model
    ) {
        logger.debug(model.toString());

        var result = new ArrayList<Runnable>(variables.size());

        logger.debug(variables.toString());

        for (var variable : variables) {
            var path = variable.variable().split(TREE_PATTERN);

            if (variable.distribution().isRealDistribution()) {
                var distribution = variable.getRealDistribution(new JDKRandomGenerator(rng.nextInt()));
                result.add(() -> model.doubleInputs().get(path).send(distribution.sample()));
            } else if (variable.distribution().isIntegerDistribution()) {
                var distribution = variable.getIntegerDistribution(new JDKRandomGenerator(rng.nextInt()));
                result.add(() -> model.intInputs().get(path).send(distribution.sample()));
            }
        }

        return result;
    }

    private Set<Integer> getAffectedAlternatives(
            List<UncertaintyVariable> variables,
            Map<Integer, Set<Integer>> bcnAltIDs,
            List<Integer> altIDs
    ) {
        var result = new HashSet<Integer>();

        for (var variable : variables) {
            var path = variable.variable().split(TREE_PATTERN);
            if (path[0].equals("bcnObjects")) {
                var bcnID = Integer.parseInt(path[1]);
                result.addAll(bcnAltIDs.getOrDefault(bcnID, Set.of()));
            } else if (path[0].equals("analysisObject")) {
                result.addAll(altIDs);
            }
        }

        return result;
    }

    @SuppressWarnings("unchecked")
    private List<Uncertainty> getUncertaintyFromInput(Map<String, Object> extensions) {
        return (List<Uncertainty>) extensions.getOrDefault("uncertainty", List.of());
    }

    private static JDKRandomGenerator getRNG(@Nullable Integer seed) {
        if (seed == null)
            return new JDKRandomGenerator();

        return new JDKRandomGenerator(seed);
    }
}
