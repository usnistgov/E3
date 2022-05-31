package gov.nist.e3.stream;

import nz.sodium.StreamSink;

public class PercentDifferenceStream extends StreamSink<Double> {
    private final double value;
    private final double percentage;
    private final boolean positive;
    private final boolean negative;

    public PercentDifferenceStream(double value, double percentage, boolean positive, boolean negative) {
        this.value = value;
        this.percentage = percentage;
        this.positive = positive;
        this.negative = negative;
    }

    public void next() {
        if (positive) {
            this.send(value * (1.0 + percentage));
        }

        if (negative) {
            this.send(value * (1.0 - percentage));
        }
    }
}
