package gov.nist.eee.pipeline.uncertainty;

import nz.sodium.Cell;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StopCondition {
    private static final Logger logger = LoggerFactory.getLogger(StopCondition.class);
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
