package gov.nist.e3.objects.input;

public enum DistributionType {
    NORMAL(true),
    GAUSSIAN(true),

    EXPONENTIAL(true),

    TRIANGULAR(true),

    UNIFORM(true),
    RECTANGULAR(true),

    ENUMERATED(true),
    DISCRETE(true),

    BETA(true),

    LOG_NORMAL(true),

    WEIBULL(true),
    EXTREME_VALUE_TYPE_III(true),

    BINOMIAL(false);

    private final boolean real;

    DistributionType(boolean real){
        this.real = real;
    }

    public boolean isRealDistribution() {
        return real;
    }

    public boolean isIntegerDistribution() {
        return !real;
    }
}
