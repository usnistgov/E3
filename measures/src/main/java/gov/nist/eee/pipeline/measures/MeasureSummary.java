package gov.nist.eee.pipeline.measures;

import org.jetbrains.annotations.Nullable;

import java.util.Map;

public record MeasureSummary(
        int altId,
        Double totalBenefits,
        Double totalCosts,
        Double totalCostsInvest,
        Double totalCostNonInvest,
        Map<String, Double> totalTagFlows,
        @Nullable Double netBenefits,
        @Nullable Double netSavings,
        @Nullable Double sir,
        @Nullable Double irr,
        Double airr,
        @Nullable Double dpp,
        @Nullable Double spp,
        @Nullable Double bcr,
        Map<String, Double> quantitySum,
        Map<String, String> quantityUnits,
        Double marr,
        @Nullable Map<String, Double> deltaQuantity,
        @Nullable Map<String, Double> nsPercentQuantity,
        @Nullable Map<String, Double> nsDeltaQuantity,
        @Nullable Map<String, Double> nsElasticityQuantity
) {
}