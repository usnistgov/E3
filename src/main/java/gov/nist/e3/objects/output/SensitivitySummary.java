package gov.nist.e3.objects.output;

import gov.nist.e3.util.Util;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public record SensitivitySummary(
        int id,
        int altId,
        List<Double> totalBenefits,
        List<Double> totalCosts,
        List<Double> totalCostsInvest,
        List<Double> totalCostNonInvest,
        Map<String, List<Double>> totalTagFlows,
        List<Double> netBenefits,
        List<Double> netSavings,
        List<Double> sir,
        List<Double> irr,
        List<Double> airr,
        List<Double> dpp,
        List<Double> spp,
        List<Double> bcr,
        Map<String, List<Double>> quantitySum,
        Map<String, List<String>> quantityUnits,
        List<Double> marr,
        Map<String, List<Double>> deltaQuantity,
        Map<String, List<Double>> nsPercentQuantity,
        Map<String, List<Double>> nsDeltaQuantity,
        Map<String, List<Double>> nsElasticityQuantity
) {
    public static SensitivitySummary of(int id, MeasureSummary summary) {
        return new SensitivitySummary(
                id,
                summary.altId(),
                Util.createList(summary.totalBenefits()),
                Util.createList(summary.totalCosts()),
                Util.createList(summary.totalCostsInvest()),
                Util.createList(summary.totalCostNonInvest()),
                toMapList(summary.totalTagFlows()),
                Util.createList(summary.netBenefits()),
                Util.createList(summary.netSavings()),
                Util.createList(summary.sir()),
                Util.createList(summary.irr()),
                Util.createList(summary.airr()),
                Util.createList(summary.dpp()),
                Util.createList(summary.spp()),
                Util.createList(summary.bcr()),
                toMapList(summary.quantitySum()),
                toMapList(summary.quantityUnits()),
                Util.createList(summary.marr()),
                toMapList(summary.deltaQuantity()),
                toMapList(summary.nsPercentQuantity()),
                toMapList(summary.nsDeltaQuantity()),
                toMapList(summary.nsElasticityQuantity())
        );
    }

    public void addMeasureSummary(MeasureSummary summary) {
        if (summary.altId() != this.altId())
            throw new IllegalArgumentException("Cannot add measure summary to sensitivity summary with different alt IDs");

        this.totalBenefits.add(summary.totalBenefits());
        this.totalCosts.add(summary.totalCosts());
        this.totalCostsInvest.add(summary.totalCostsInvest());
        this.totalCostNonInvest.add(summary.totalCostNonInvest());

        addEntries(summary.totalTagFlows(), this.totalTagFlows());

        this.netBenefits.add(summary.netBenefits());
        this.netSavings.add(summary.netSavings());
        this.sir.add(summary.sir());
        this.irr.add(summary.irr());
        this.airr.add(summary.airr());
        this.dpp.add(summary.dpp());
        this.spp.add(summary.spp());
        this.bcr.add(summary.bcr());

        addEntries(summary.quantitySum(), this.quantitySum());
        addEntries(summary.quantityUnits(), this.quantityUnits());

        this.marr.add(summary.marr());

        addEntries(summary.deltaQuantity(), this.deltaQuantity());
        addEntries(summary.nsPercentQuantity(), this.nsPercentQuantity());
        addEntries(summary.nsDeltaQuantity(), this.nsDeltaQuantity());
        addEntries(summary.nsElasticityQuantity(), this.nsElasticityQuantity());
    }

    private static <A, B> void addEntries(Map<A, B> toAdd, Map<A, List<B>> to) {
        if (toAdd == null)
            return;

        for (var entry : toAdd.entrySet()) {
            to.get(entry.getKey()).add(entry.getValue());
        }
    }

    private static <A, B> Map<A, List<B>> toMapList(Map<A, B> original) {
        var result = new HashMap<A, List<B>>();

        if (original != null) {
            for (var entry : original.entrySet()) {
                result.put(entry.getKey(), Util.createList(entry.getValue()));
            }
        }

        return result;
    }
}
