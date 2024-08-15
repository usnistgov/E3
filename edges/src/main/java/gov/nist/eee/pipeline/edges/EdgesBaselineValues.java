package gov.nist.eee.pipeline.edges;

import java.util.List;

public record EdgesBaselineValues(
        List<Double> costsNonDiscounted,
        List<Double> benefitsNonDiscounted,
        List<Double> externalNonDiscounted,
        double npvInvestCosts,
        double npvBenefits,
        double npvNonInvestCosts,
        double external,
        double npvDisasterDiscount
) {
}
