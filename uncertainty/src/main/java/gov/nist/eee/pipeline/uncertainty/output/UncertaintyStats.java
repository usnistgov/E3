package gov.nist.eee.pipeline.uncertainty.output;

import org.apache.commons.math3.stat.descriptive.SummaryStatistics;

public record UncertaintyStats(double standardDeviation, double mean) {
    public UncertaintyStats(final SummaryStatistics stats) {
        this(stats.getStandardDeviation(), stats.getMean());
    }
}