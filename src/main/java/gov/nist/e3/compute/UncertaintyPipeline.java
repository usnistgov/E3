package gov.nist.e3.compute;

import gov.nist.e3.Config;
import gov.nist.e3.objects.input.Bcn;
import gov.nist.e3.objects.input.Uncertainty;
import gov.nist.e3.objects.output.*;
import gov.nist.e3.tree.Tree;
import nz.sodium.*;
import org.apache.commons.math3.random.JDKRandomGenerator;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

public class UncertaintyPipeline {
    private static final Logger log = LoggerFactory.getLogger(UncertaintyPipeline.class);

    private final List<Uncertainty> uncertainties;
    private final Tree<String, CellSink<? extends Number>> cellTree;
    private final Map<Integer, MeasureSummaryPipeline> measureSummaries;
    private final Map<Integer, Bcn> bcns;
    private final Set<Integer> altIDs;

    public UncertaintyPipeline(
            List<Uncertainty> uncertainties,
            Tree<String, CellSink<? extends Number>> cellTree,
            Map<Integer, MeasureSummaryPipeline> measureSummaries,
            Map<Integer, Bcn> bcns,
            Set<Integer> altIDs
    ) {
        this.uncertainties = uncertainties;
        this.cellTree = cellTree;
        this.measureSummaries = measureSummaries;
        this.bcns = bcns;
        this.altIDs = altIDs;
    }

    public List<UncertaintySummary> analyze() {
        var result = new ArrayList<UncertaintySummary>(uncertainties.size());

        for (var uncertainty : uncertainties) {
            var distributions = new ArrayList<Runnable>();

            var seed = uncertainty.seed();
            var rng = seed != null ? new JDKRandomGenerator(seed) : new JDKRandomGenerator();

            var affectedAlternativeIDs = new HashSet<Integer>();

            for (var variable : uncertainty.variables()) {
                var path = variable.variable().split(Config.TREE_PATTERN);

                if(path[0].equals("bcnObjects")) {
                    var bcnID = Integer.parseInt(path[1]);
                    affectedAlternativeIDs.addAll(bcns.get(bcnID).altIds());
                } else if(path[0].equals("analysisObject")) {
                    affectedAlternativeIDs.addAll(altIDs);
                }

                var cell = (CellSink<Number>) cellTree.get(variable.variable().split(Config.TREE_PATTERN));

                if (variable.distribution().isRealDistribution()) {
                    var distribution = variable.getRealDistribution(new JDKRandomGenerator(rng.nextInt()));
                    distributions.add(() -> cell.send(distribution.sample()));
                } else if (variable.distribution().isIntegerDistribution()) {
                    var distribution = variable.getIntegerDistribution(new JDKRandomGenerator(rng.nextInt()));
                    distributions.add(() -> cell.send(distribution.sample()));
                }
            }

            log.debug("Affected alternatives {}", affectedAlternativeIDs);

            var summaries = measureSummaries.entrySet()
                    .stream()
                    .filter(e -> affectedAlternativeIDs.contains(e.getKey()))
                    .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

            var output = run(uncertainty.id(), summaries, distributions);
            result.add(new UncertaintySummary(uncertainty.id(), output));
        }

        return result;
    }

    private Map<Integer, UncertaintyMeasureSummary> run(
            int id,
            Map<Integer, MeasureSummaryPipeline> measureSummaryPipelines,
            List<Runnable> distributions
    ) {
        log.debug("Running uncertainty transactions");

        var stopConditions = new ArrayList<StopCondition>(measureSummaryPipelines.size() * 4);
        var builders = new ArrayList<UncertaintySummaryBuilder>(measureSummaryPipelines.size());

        for(var entry : measureSummaryPipelines.entrySet()) {
            var altId = entry.getKey();
            var summary = entry.getValue();

            stopConditions.addAll(List.of(
                    createMeasureStopCondition(summary, MeasureSummary::totalCosts),
                    createMeasureStopCondition(summary, MeasureSummary::totalBenefits),
                    createMeasureStopCondition(summary, MeasureSummary::totalCostsInvest),
                    createMeasureStopCondition(summary, MeasureSummary::totalCostNonInvest)
            ));

            builders.add(new UncertaintySummaryBuilder(id, altId).bindMeasureSummary(summary));
        }

        for (var i = 0; i < Config.UNCERTAINTY_MAX_ITERATIONS && (i < 5000 || i % 500 != 0 || !stopConditions.stream().allMatch(StopCondition::shouldStop)); i++) {
            runTransaction(distributions);
            stopConditions.forEach(StopCondition::update);
            //log.debug("iteration {}", i);
        }

        return builders.stream().collect(
                Collectors.toMap(UncertaintySummaryBuilder::getAltID, UncertaintySummaryBuilder::build)
        );
    }

    private StopCondition createMeasureStopCondition(MeasureSummaryPipeline summary, Lambda1<MeasureSummary, Double> getter)  {
        return new StopCondition(summary.cMeasureSummary.map(getter), Config.UNCERTAINTY_TOLERANCE);
    }

    private void runTransaction(List<Runnable> distributions) {
        Transaction.runVoid(() -> {
            for (var distribution : distributions) {
                distribution.run();
            }
        });
    }

    static final class StopCondition {
        private final Cell<Double> cell;

        private final SummaryStatistics statistics = new SummaryStatistics();
        private double previous;
        private double current = 0.0;

        private final double tolerance;

        public StopCondition(Cell<Double> cell, double tolerance) {
            this.cell = cell;
            this.tolerance = tolerance;

            statistics.addValue(cell.sample());
            previous = statistics.getMean();
        }

        public void update() {
            previous = statistics.getMean();
            statistics.addValue(cell.sample());
            current = statistics.getMean();
        }

        public boolean shouldStop() {
            if (previous == 0)
                return Math.abs(current) <= tolerance;

            return Math.abs(previous - current) / previous <= tolerance;
        }

        public double getMean() {
            return statistics.getMean();
        }

        public double getStandardDeviation() {
            return statistics.getStandardDeviation();
        }
    }
}
