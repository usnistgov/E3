package gov.nist.e3.objects.input;

import gov.nist.e3.util.Util;
import org.apache.commons.math3.distribution.*;
import org.apache.commons.math3.random.RandomGenerator;

import java.util.ArrayList;
import java.util.List;

public record UncertaintyVariable(String variable, DistributionType distribution, List<List<Number>> distributionArgs) {
    private List<Object> getDistributionArgList(RandomGenerator rng) {
        if (distributionArgs == null)
            throw new IllegalArgumentException("Distribution arguments cannot be null");

        var result = new ArrayList<>();

        result.add(rng);

        for (var arg : distributionArgs) {
            if (arg.size() > 1)
                result.add(arg.toArray());
            else if (arg.size() == 1)
                result.add(arg.get(0));
            else
                throw new IllegalArgumentException("Cannot use distribution function argument " + arg);
        }

        return result;
    }

    public RealDistribution getRealDistribution(RandomGenerator rng) {
        var args = getDistributionArgList(rng);

        return switch (distribution) {
            case NORMAL, GAUSSIAN -> Util.getInstanceFromArgCount(NormalDistribution.class, args);
            case EXPONENTIAL -> Util.getInstanceFromArgCount(ExponentialDistribution.class, args);
            case TRIANGULAR -> Util.getInstanceFromArgCount(TriangularDistribution.class, args);
            case UNIFORM, RECTANGULAR -> Util.getInstanceFromArgCount(UniformRealDistribution.class, args);
            case ENUMERATED, DISCRETE -> Util.getInstanceFromArgCount(EnumeratedRealDistribution.class, args);
            case BETA -> Util.getInstanceFromArgCount(BetaDistribution.class, args);
            case LOG_NORMAL -> Util.getInstanceFromArgCount(LogNormalDistribution.class, args);
            case WEIBULL, EXTREME_VALUE_TYPE_III -> Util.getInstanceFromArgCount(WeibullDistribution.class, args);
            default ->
                    throw new IllegalArgumentException("Distribution type \"" + distribution + "\" is not a real distribution.");
        };
    }

    public IntegerDistribution getIntegerDistribution(RandomGenerator rng) {
        var args = getDistributionArgList(rng);

        if (distribution == DistributionType.BINOMIAL)
            return Util.getInstanceFromArgCount(BinomialDistribution.class, args);

        throw new IllegalArgumentException("Distribution type \"" + distribution + "\" is not an integer distribution.");
    }
}
