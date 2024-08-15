package gov.nist.eee.pipeline.uncertainty;


import gov.nist.eee.pipeline.measures.MeasureSummary;
import gov.nist.eee.pipeline.uncertainty.output.UncertaintyMeasureSummary;
import gov.nist.eee.pipeline.uncertainty.output.UncertaintyStats;
import nz.sodium.Cell;
import nz.sodium.Lambda1;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

public class UncertaintySummaryBuilder {
    private int id;
    private int altID;

    private SummaryStatistics totalCostsStats;
    private SummaryStatistics totalBenefitsStats;
    private SummaryStatistics totalCostsInvestStats;
    private SummaryStatistics totalCostsNonInvestStats;
    private Map<String, SummaryStatistics> totalTagFlowStats;
    private SummaryStatistics netBenefitsStats;
    private SummaryStatistics netSavingsStats;
    private SummaryStatistics sirStats;
    private SummaryStatistics airrStats;
    private SummaryStatistics dppStats;
    private SummaryStatistics sppStats;
    private SummaryStatistics irrStats;
    private SummaryStatistics bcrStats;
    private Map<String, SummaryStatistics> quantitySumStats;
    private Map<String, SummaryStatistics> deltaQuantityStats;
    private Map<String, SummaryStatistics> nsPercentQuantityStats;
    private Map<String, SummaryStatistics> nsDeltaQuantityStats;
    private Map<String, SummaryStatistics> nsElasticityQuantityStats;

    public UncertaintySummaryBuilder(int id, int altId) {
        this.id = id;
        this.altID = altId;
    }

    public UncertaintySummaryBuilder bindMeasureSummary(Cell<MeasureSummary> cMeasureSummary) {
        totalCostsStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::totalCosts);
        totalBenefitsStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::totalBenefits);
        totalCostsInvestStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::totalCostsInvest);
        totalCostsNonInvestStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::totalCostNonInvest);

        totalTagFlowStats = new HashMap<>();
        for (var entry : cMeasureSummary.map(MeasureSummary::totalTagFlows).sample().entrySet()) {
            var key = entry.getKey();
            totalTagFlowStats.put(key, bindSummaryStatistics(cMeasureSummary, v -> v.totalTagFlows().get(key)));
        }

        netBenefitsStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::netBenefits);
        netSavingsStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::netSavings);
        sirStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::sir);
        airrStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::airr);
        dppStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::dpp);
        sppStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::spp);
        irrStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::irr);
        bcrStats = bindSummaryStatistics(cMeasureSummary, MeasureSummary::bcr);

        quantitySumStats = new HashMap<>();
        for (var entry : cMeasureSummary.map(MeasureSummary::quantitySum).sample().entrySet()) {
            var key = entry.getKey();
            quantitySumStats.put(key, bindSummaryStatistics(cMeasureSummary, v -> v.quantitySum().get(key)));
        }

        var deltaQuantity = cMeasureSummary.map(MeasureSummary::deltaQuantity).sample();
        if (deltaQuantity != null) {
            deltaQuantityStats = new HashMap<>();
            for (var entry : deltaQuantity.entrySet()) {
                var key = entry.getKey();
                deltaQuantityStats.put(key, bindSummaryStatistics(cMeasureSummary, v -> {
                    var value = v.deltaQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            deltaQuantityStats = null;
        }

        var nsPercentQuantity = cMeasureSummary.map(MeasureSummary::nsPercentQuantity).sample();
        if (nsPercentQuantity != null) {
            nsPercentQuantityStats = new HashMap<>();
            for (var entry : nsPercentQuantity.entrySet()) {
                var key = entry.getKey();
                nsPercentQuantityStats.put(key, bindSummaryStatistics(cMeasureSummary, v -> {
                    var value = v.nsPercentQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            nsPercentQuantityStats = null;
        }

        var nsDeltaQuantity = cMeasureSummary.map(MeasureSummary::nsDeltaQuantity).sample();
        if (nsDeltaQuantity != null) {
            nsDeltaQuantityStats = new HashMap<>();
            for (var entry : nsDeltaQuantity.entrySet()) {
                var key = entry.getKey();
                nsDeltaQuantityStats.put(key, bindSummaryStatistics(cMeasureSummary, v -> {
                    var value = v.nsDeltaQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            nsDeltaQuantityStats = null;
        }

        var nsElasticityQuantity = cMeasureSummary.map(MeasureSummary::nsElasticityQuantity).sample();
        if (nsElasticityQuantity != null) {
            nsElasticityQuantityStats = new HashMap<>();
            for (var entry : nsElasticityQuantity.entrySet()) {
                var key = entry.getKey();
                nsElasticityQuantityStats.put(key, bindSummaryStatistics(cMeasureSummary, v -> {
                    var value = v.nsElasticityQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            nsElasticityQuantityStats = null;
        }

        return this;
    }

    public int getAltID() {
        return this.altID;
    }

    public UncertaintyMeasureSummary build() {
        return new UncertaintyMeasureSummary(
                new UncertaintyStats(totalBenefitsStats),
                new UncertaintyStats(totalCostsStats),
                new UncertaintyStats(totalCostsInvestStats),
                new UncertaintyStats(totalCostsNonInvestStats),
                totalTagFlowStats.entrySet()
                        .stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, e -> new UncertaintyStats(e.getValue()))),
                new UncertaintyStats(netBenefitsStats),
                new UncertaintyStats(netSavingsStats),
                new UncertaintyStats(sirStats),
                new UncertaintyStats(irrStats),
                new UncertaintyStats(airrStats),
                new UncertaintyStats(dppStats),
                new UncertaintyStats(sppStats),
                new UncertaintyStats(bcrStats),
                quantitySumStats.entrySet()
                        .stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, e -> new UncertaintyStats(e.getValue()))),
                deltaQuantityStats == null ? null : deltaQuantityStats.entrySet()
                        .stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, e -> new UncertaintyStats(e.getValue()))),
                nsPercentQuantityStats == null ? null : nsPercentQuantityStats.entrySet()
                        .stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, e -> new UncertaintyStats(e.getValue()))),
                nsDeltaQuantityStats == null ? null : nsDeltaQuantityStats.entrySet()
                        .stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, e -> new UncertaintyStats(e.getValue()))),
                nsElasticityQuantityStats == null ? null : nsElasticityQuantityStats.entrySet()
                        .stream()
                        .collect(Collectors.toMap(Map.Entry::getKey, e -> new UncertaintyStats(e.getValue())))
        );
    }

    private SummaryStatistics bindSummaryStatistics(
            Cell<MeasureSummary> cMeasureSummary,
            Lambda1<MeasureSummary, Double> getter
    ) {
        var result = new SummaryStatistics();
        cMeasureSummary.map(getter).listen(v -> {
            if (v != null)
                result.addValue(v);
        });
        return result;
    }
}