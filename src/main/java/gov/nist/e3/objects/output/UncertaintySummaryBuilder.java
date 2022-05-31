package gov.nist.e3.objects.output;

import gov.nist.e3.compute.MeasureSummaryPipeline;
import nz.sodium.Lambda1;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;
import org.springframework.boot.info.InfoProperties;

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

    public UncertaintySummaryBuilder bindMeasureSummary(MeasureSummaryPipeline summary) {
        totalCostsStats = bindSummaryStatistics(summary, MeasureSummary::totalCosts);
        totalBenefitsStats = bindSummaryStatistics(summary, MeasureSummary::totalBenefits);
        totalCostsInvestStats = bindSummaryStatistics(summary, MeasureSummary::totalCostsInvest);
        totalCostsNonInvestStats = bindSummaryStatistics(summary, MeasureSummary::totalCostNonInvest);

        totalTagFlowStats = new HashMap<>();
        for (var entry : summary.cMeasureSummary.map(MeasureSummary::totalTagFlows).sample().entrySet()) {
            var key = entry.getKey();
            totalTagFlowStats.put(key, bindSummaryStatistics(summary, v -> v.totalTagFlows().get(key)));
        }

        netBenefitsStats = bindSummaryStatistics(summary, MeasureSummary::netBenefits);
        netSavingsStats = bindSummaryStatistics(summary, MeasureSummary::netSavings);
        sirStats = bindSummaryStatistics(summary, MeasureSummary::sir);
        airrStats = bindSummaryStatistics(summary, MeasureSummary::airr);
        dppStats = bindSummaryStatistics(summary, MeasureSummary::dpp);
        sppStats = bindSummaryStatistics(summary, MeasureSummary::spp);
        irrStats = bindSummaryStatistics(summary, MeasureSummary::irr);
        bcrStats = bindSummaryStatistics(summary, MeasureSummary::bcr);

        quantitySumStats = new HashMap<>();
        for (var entry : summary.cMeasureSummary.map(MeasureSummary::quantitySum).sample().entrySet()) {
            var key = entry.getKey();
            quantitySumStats.put(key, bindSummaryStatistics(summary, v -> v.quantitySum().get(key)));
        }

        var deltaQuantity = summary.cMeasureSummary.map(MeasureSummary::deltaQuantity).sample();
        if (deltaQuantity != null) {
            deltaQuantityStats = new HashMap<>();
            for (var entry : deltaQuantity.entrySet()) {
                var key = entry.getKey();
                deltaQuantityStats.put(key, bindSummaryStatistics(summary, v -> {
                    var value = v.deltaQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            deltaQuantityStats = null;
        }

        var nsPercentQuantity = summary.cMeasureSummary.map(MeasureSummary::nsPercentQuantity).sample();
        if (nsPercentQuantity != null) {
            nsPercentQuantityStats = new HashMap<>();
            for (var entry : nsPercentQuantity.entrySet()) {
                var key = entry.getKey();
                nsPercentQuantityStats.put(key, bindSummaryStatistics(summary, v -> {
                    var value = v.nsPercentQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            nsPercentQuantityStats = null;
        }

        var nsDeltaQuantity = summary.cMeasureSummary.map(MeasureSummary::nsDeltaQuantity).sample();
        if (nsDeltaQuantity != null) {
            nsDeltaQuantityStats = new HashMap<>();
            for (var entry : nsDeltaQuantity.entrySet()) {
                var key = entry.getKey();
                nsDeltaQuantityStats.put(key, bindSummaryStatistics(summary, v -> {
                    var value = v.nsDeltaQuantity();

                    if (value != null)
                        return value.get(key);

                    return 0.0;
                }));
            }
        } else {
            nsDeltaQuantityStats = null;
        }

        var nsElasticityQuantity = summary.cMeasureSummary.map(MeasureSummary::nsElasticityQuantity).sample();
        if (nsElasticityQuantity != null) {
            nsElasticityQuantityStats = new HashMap<>();
            for (var entry : nsElasticityQuantity.entrySet()) {
                var key = entry.getKey();
                nsElasticityQuantityStats.put(key, bindSummaryStatistics(summary, v -> {
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
            MeasureSummaryPipeline summary,
            Lambda1<MeasureSummary, Double> getter
    ) {
        var result = new SummaryStatistics();
        summary.cMeasureSummary.map(getter).listen(v -> {
            if (v != null)
                result.addValue(v);
        });
        return result;
    }
}
