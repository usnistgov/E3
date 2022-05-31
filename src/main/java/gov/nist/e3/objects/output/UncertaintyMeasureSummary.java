package gov.nist.e3.objects.output;

import org.jetbrains.annotations.Nullable;

import java.util.Map;

public record UncertaintyMeasureSummary(
        UncertaintyStats totalBenefits,
        UncertaintyStats totalCosts,
        UncertaintyStats totalCostsInvest,
        UncertaintyStats totalCostNonInvest,
        Map<String, UncertaintyStats> totalTagFlows,
        @Nullable UncertaintyStats netBenefits,
        @Nullable UncertaintyStats netSavings,
        @Nullable UncertaintyStats sir,
        @Nullable UncertaintyStats irr,
        UncertaintyStats airr,
        @Nullable UncertaintyStats dpp,
        @Nullable UncertaintyStats spp,
        @Nullable UncertaintyStats bcr,
        Map<String, UncertaintyStats> quantitySum,
        @Nullable Map<String, UncertaintyStats> deltaQuantity,
        @Nullable Map<String, UncertaintyStats> nsPercentQuantity,
        @Nullable Map<String, UncertaintyStats> nsDeltaQuantity,
        @Nullable Map<String, UncertaintyStats> nsElasticityQuantity
) {
}
