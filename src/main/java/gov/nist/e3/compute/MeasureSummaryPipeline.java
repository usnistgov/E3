package gov.nist.e3.compute;

import gov.nist.e3.formula.Formula;
import gov.nist.e3.objects.output.MeasureSummary;
import gov.nist.e3.objects.output.OptionalCashflow;
import gov.nist.e3.objects.output.RequiredCashflow;
import gov.nist.e3.util.CellUtils;
import gov.nist.e3.util.Util;
import gov.nist.e3.util.tuple.Tuple3;
import gov.nist.e3.util.tuple.Tuple6;
import nz.sodium.Cell;
import nz.sodium.Transaction;
import org.apache.commons.math3.exception.NoBracketingException;
import org.jetbrains.annotations.Nullable;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

public class MeasureSummaryPipeline {
    public final Cell<MeasureSummary> cMeasureSummary;

    private Cell<Double> cTotalBenefits;
    private Cell<Double> cTotalCosts;
    private Cell<Double> cTotalCostsInvest;
    private Cell<Double> cTotalCostsNonInvest;
    private Cell<Double> cNetBenefits;
    private Cell<Map<String, Double>> cQuantitySum;
    private Cell<@Nullable Map<String, Double>> cDeltaQuantity;
    private final RequiredCashflowPipeline required;

    public MeasureSummaryPipeline(
            Cell<Double> cReinvestRate,
            Cell<Integer> cStudyPeriod,
            Cell<Double> cMarr,
            RequiredCashflowPipeline required,
            List<OptionalCashflowPipeline> optionals,
            @Nullable MeasureSummaryPipeline baseline,
            @Nullable RequiredCashflowPipeline baselineRequiredFlow
    ) {
        this.required = required;

        cMeasureSummary = define(cReinvestRate, cStudyPeriod, cMarr, required, optionals, baseline, baselineRequiredFlow);
    }

    private Cell<MeasureSummary> define(
            Cell<Double> cReinvestRate,
            Cell<Integer> cStudyPeriod,
            Cell<Double> cMarr,
            RequiredCashflowPipeline required,
            List<OptionalCashflowPipeline> optionals,
            @Nullable MeasureSummaryPipeline baseline,
            @Nullable RequiredCashflowPipeline baselineRequiredFlow
    ) {
        return Transaction.run(() -> {
            var cRequiredCashflow = required.cRequiredCashflow;

            var cFlattenedOptionals = CellUtils.sequence(
                    optionals.stream()
                            .map(optional -> optional.cOptionalCashflows)
                            .toList()
            );

            var cAltId = cRequiredCashflow.map(RequiredCashflow::altId);

            cTotalBenefits = cRequiredCashflow
                    .map(RequiredCashflow::totalBenefitsDiscounted)
                    .map(Util::sum);

            cTotalCosts = cRequiredCashflow
                    .map(RequiredCashflow::totalCostsDiscounted)
                    .map(Util::sum);

            cTotalCostsInvest = cRequiredCashflow
                    .map(RequiredCashflow::totalCostsDiscountedInvest)
                    .map(Util::sum);

            cTotalCostsNonInvest = cRequiredCashflow
                    .map(RequiredCashflow::totalCostsDiscountedNonInvest)
                    .map(Util::sum);

            var cTotalTagFlows = cFlattenedOptionals.map(
                    Util.toMap(OptionalCashflow::tag, OptionalCashflow::totalTagCashflowDiscounted, Util::sum)
            );

            Cell<@Nullable MeasureSummaryPipeline> cBaseline = CellUtils.liftNullable(baseline);

            Cell<@Nullable RequiredCashflow> cBaselineRequiredCashflow = CellUtils.nullableFlatMap(
                    CellUtils.liftNullable(baselineRequiredFlow), RequiredCashflowPipeline::cRequiredCashflow
            );

            var cBaselineTotalBenefits = CellUtils.nullableFlatMap(cBaseline, base -> base.cTotalBenefits);

            cNetBenefits = CellUtils.nullableFlatMap(
                    cBaseline, base -> netBenefits(cTotalBenefits, cTotalCosts, base.cTotalBenefits, base.cTotalCosts)
            );

            Cell<@Nullable Double> cNetSavings = CellUtils.nullableFlatMap(
                    cBaseline, base -> netSavings(cTotalCosts, base.cTotalCosts)
            );


            Cell<@Nullable Double> cSir = CellUtils.nullableFlatMap(cBaseline, sirFromBaseline(cTotalCostsNonInvest, cTotalCostsInvest));

            var cTotalNonDiscounted = cRequiredCashflow.map(RequiredCashflow::totalBenefitsNonDiscounted)
                    .lift(cRequiredCashflow.map(RequiredCashflow::totalCostsNonDiscounted), Util::elementwiseSubtract);
            Cell<@Nullable List<Double>> cBaselineTotalNonDiscounted = CellUtils.nullableFlatMap(
                    cBaseline,
                    x -> x.required
                            .cRequiredCashflow
                            .map(RequiredCashflow::totalCostsNonDiscounted)
                            .lift(
                                    x.required.cRequiredCashflow.map(RequiredCashflow::totalBenefitsNonDiscounted),
                                    Util::elementwiseSubtract
                            )
            );

            Cell<Double> cIrr = CellUtils.nullableFlatMap(
                    cBaselineTotalNonDiscounted,
                    baselineValues -> cTotalNonDiscounted.map(v -> Util.elementwiseAdd(v, baselineValues))
                            .map(values -> {
                                try {
                                    return Formula.irr(values);
                                } catch (NoBracketingException e) {
                                    return null;
                                }
                            })
            );

            Cell<@Nullable Double> cAirr = cSir.lift(
                    cReinvestRate,
                    cStudyPeriod,
                    (sir, reinvestRate, studyPeriod) -> sir == null ? Double.NaN : airr(sir, reinvestRate, studyPeriod)
            );

            Cell<@Nullable Double> cSpp = required.cRequiredCashflow.lift(
                    cBaselineRequiredCashflow,
                    (requiredFlow, baselineFlow) -> {
                        if (baselineFlow == null)
                            return null;

                        return paybackPeriod(
                                requiredFlow.totalBenefitsNonDiscounted(),
                                baselineFlow.totalBenefitsNonDiscounted(),
                                baselineFlow.totalCostsNonDiscounted(),
                                requiredFlow.totalCostsNonDiscounted()
                        );
                    }
            );

            Cell<@Nullable Double> cDpp = required.cRequiredCashflow.lift(
                    cBaselineRequiredCashflow,
                    (requiredFlow, baselineFlow) -> {
                        if (baselineFlow == null)
                            return null;

                        return paybackPeriod(
                                requiredFlow.totalBenefitsDiscounted(),
                                baselineFlow.totalBenefitsDiscounted(),
                                baselineFlow.totalCostsDiscounted(),
                                requiredFlow.totalCostsDiscounted()
                        );
                    }
            );

            Cell<@Nullable Double> cTotalCostsInvestBaseline = CellUtils.nullableFlatMap(cBaseline, base -> base.cTotalCostsInvest);
            Cell<@Nullable Double> cTotalCostsNonInvestBaseline = CellUtils.nullableFlatMap(cBaseline, base -> base.cTotalCostsNonInvest);

            Cell<@Nullable Double> cBcr = cTotalCostsInvestBaseline.lift(
                    cTotalBenefits,
                    cTotalCostsInvest,
                    cTotalCostsNonInvest,
                    cTotalCostsNonInvestBaseline,
                    cBaselineTotalBenefits,
                    (totalCostsInvestBaseline, netBenefits, totalCostsInvest, totalCostsNonInvest, totalCostsNonInvestBaseline, netBenefitsBaseline) -> {
                        if (totalCostsInvestBaseline == null || netBenefits == null || totalCostsNonInvestBaseline == null)
                            return null;

                        var benefitBaseline = netBenefitsBaseline == null ? 0.0 : netBenefitsBaseline;

                        return this.bcr(netBenefits, benefitBaseline, totalCostsInvest, totalCostsInvestBaseline, totalCostsNonInvest, totalCostsNonInvestBaseline);
                    });

            cQuantitySum = cFlattenedOptionals.map(
                    Util.toMap(OptionalCashflow::tag, OptionalCashflow::totalTagQuantity, Util::sum)
            );

            var cQuantityUnits = cFlattenedOptionals.map(
                    Util.toMap(OptionalCashflow::tag, OptionalCashflow::units)
            );

            cDeltaQuantity = CellUtils.nullableFlatMap(cBaseline, base -> deltaQuantity(optionals, base.cQuantitySum));

            Cell<@Nullable Map<String, Double>> baselineQuantitySums = CellUtils.nullableFlatMap(cBaseline, base -> base.cQuantitySum);

            Cell<@Nullable Map<String, Double>> cNsPercentQuantity = cNetSavings.lift(
                    cFlattenedOptionals,
                    baselineQuantitySums,
                    (netSavings, optionalCashflows, baseSums) -> {
                        if (baseSums == null)
                            return null;

                        return nsPercentQuantity(netSavings, optionalCashflows, baseSums);
                    }
            );

            Cell<@Nullable Map<String, Double>> baselineDeltaQuantity = CellUtils.nullableFlatMap(cBaseline, base -> base.cDeltaQuantity);

            Cell<@Nullable Map<String, Double>> cNsDeltaQuantity = cNetSavings.lift(
                    cFlattenedOptionals,
                    baselineDeltaQuantity,
                    (netSavings, optionalCashflows, baseDeltaQuantity) -> {
                        if (baseDeltaQuantity == null)
                            return null;

                        return nsDeltaQuantity(netSavings, optionalCashflows, baseDeltaQuantity);
                    }
            );

            Cell<@Nullable Map<String, Double>> cNsElasticityQuantity = cNetSavings.lift(
                    cTotalCosts,
                    cFlattenedOptionals,
                    baselineQuantitySums,
                    (netSavings, totalCosts, optionalCashflows, baseQuantitySum) -> {
                        if (netSavings == null || baselineQuantitySums == null)
                            return null;

                        return nsElasticityQuantity(netSavings, totalCosts, optionalCashflows, baseQuantitySum);
                    }
            );

            var cPart1 = cAltId.lift(
                    cTotalBenefits,
                    cTotalCosts,
                    cTotalCostsInvest,
                    cTotalCostsNonInvest,
                    cTotalTagFlows,
                    Tuple6::new
            );

            var cPart2 = cNetBenefits.lift(
                    cNetSavings,
                    cSir,
                    cIrr,
                    cAirr,
                    cDpp,
                    Tuple6::new
            );

            var cPart3 = cSpp.lift(
                    cBcr,
                    cQuantitySum,
                    cQuantityUnits,
                    cMarr,
                    cDeltaQuantity,
                    Tuple6::new
            );

            var cPart4 = cNsPercentQuantity.lift(
                    cNsDeltaQuantity,
                    cNsElasticityQuantity,
                    Tuple3::new
            );

            return cPart1.lift(
                    cPart2,
                    cPart3,
                    cPart4,
                    (p1, p2, p3, p4) -> new MeasureSummary(p1.e1(), p1.e2(), p1.e3(), p1.e4(), p1.e5(), p1.e6(), p2.e1(), p2.e2(), p2.e3(), p2.e4(), p2.e5(), p2.e6(), p3.e1(), p3.e2(), p3.e3(), p3.e4(), p3.e5(), p3.e6(), p4.e1(), p4.e2(), p4.e3())
            );
        });
    }

    private Map<String, Double> nsElasticityQuantity(
            Double savings,
            Double totalCosts,
            List<OptionalCashflow> optionals,
            Map<String, Double> baselineQuantitySum
    ) {
        var result = new HashMap<String, Double>();

        for (var optional : optionals) {
            var tag = optional.tag();
            var sum = Util.sum(optional.totalTagQuantity());

            result.put(tag, nsElasticity(savings, totalCosts, sum, baselineQuantitySum.getOrDefault(tag, 0.0)));
        }

        return result;
    }

    private Map<String, Double> nsDeltaQuantity(
            Double savings,
            List<OptionalCashflow> optionals,
            Map<String, Double> deltaQuantity
    ) {
        var result = new HashMap<String, Double>();

        for (var optional : optionals) {
            var tag = optional.tag();

            result.put(tag, nsPerQuantity(savings, deltaQuantity.getOrDefault(tag, 0.0)));
        }

        return result;
    }

    private Map<String, Double> nsPercentQuantity(
            double savings,
            List<OptionalCashflow> optionals,
            Map<String, Double> baselineQuantitySum
    ) {
        var result = new HashMap<String, Double>();

        for (var optional : optionals) {
            var tag = optional.tag();
            var quantitySum = Util.sum(optional.totalTagQuantity());

            result.put(tag, nsPerPercentQuantity(savings, quantitySum, baselineQuantitySum.getOrDefault(tag, 0.0)));
        }

        return result;
    }

    private double nsElasticity(double savings, double costs, double deltaQ, double baselineTotalQ) {
        if (costs == 0)
            return Double.POSITIVE_INFINITY;

        return nsPerPercentQuantity(savings / costs, deltaQ, baselineTotalQ);
    }

    private double nsPerPercentQuantity(double savings, double deltaQuantity, double baselineTotalQuantity) {
        if (baselineTotalQuantity == 0)
            return Double.POSITIVE_INFINITY;

        return nsPerQuantity(savings, deltaQuantity / baselineTotalQuantity);
    }

    private double nsPerQuantity(double savings, double deltaQuantity) {
        if (deltaQuantity == 0)
            return Double.POSITIVE_INFINITY;

        return savings / deltaQuantity;
    }

    private Cell<Map<String, Double>> deltaQuantity(
            List<OptionalCashflowPipeline> optionals,
            Cell<Map<String, Double>> baselineQuantitySum
    ) {
        return CellUtils.sequence(optionals.stream().map(pipeline -> pipeline.cOptionalCashflows).toList())
                .lift(
                        baselineQuantitySum,
                        (list, baseline) -> {
                            var result = new HashMap<String, Double>();

                            for (var optional : list) {
                                var tag = optional.tag();
                                var quantitySum = Util.sum(optional.totalTagQuantity());

                                result.put(tag, quantitySum - baseline.getOrDefault(tag, 0.0));
                            }

                            return result;
                        }
                );
    }

    private double airr(double sir, double reinvestRate, int studyPeriod) {
        if (Double.isNaN(sir) || Double.isInfinite(sir) || sir <= 0.0)
            return Double.NaN;

        return (1.0 + reinvestRate) * Math.pow(sir, 1.0 / studyPeriod) - 1;
    }

    private Function<MeasureSummaryPipeline, Cell<Double>> sirFromBaseline(Cell<Double> costsNonInvest, Cell<Double> costsInvest) {
        return baseline -> {
            var cCostsNonInvestBaseline = baseline.cMeasureSummary.map(MeasureSummary::totalCostNonInvest);
            var cCostsInvestBaseline = baseline.cMeasureSummary.map(MeasureSummary::totalCostsInvest);

            return sir(costsNonInvest, costsInvest, cCostsNonInvestBaseline, cCostsInvestBaseline);
        };
    }

    private Cell<Double> sir(Cell<Double> costsNonInvest, Cell<Double> costsInvest, Cell<Double> costsNonInvestBaseline, Cell<Double> costsInvestBaseline) {
        return costsNonInvest.lift(
                costsInvest,
                costsNonInvestBaseline,
                costsInvestBaseline,
                (a, b, c, d) -> checkFraction(c - a, b - d)
        );
    }

    private Double checkFraction(Double numerator, Double denominator) {
        if (denominator <= 0 && numerator > 0)
            return Double.POSITIVE_INFINITY;
        else if (denominator <= 0 && numerator <= 0)
            return Double.NaN;
        else
            return numerator / denominator;
    }

    private Cell<Double> netSavings(Cell<Double> costs, Cell<Double> baselineCosts) {
        return baselineCosts.lift(costs, (bc, c) -> bc - c);
    }

    private Cell<Double> netBenefits(
            Cell<Double> totalBenefits,
            Cell<Double> totalCosts,
            Cell<Double> baselineTotalBenefits,
            Cell<Double> baselineTotalCosts
    ) {
        return totalBenefits.lift(
                totalCosts,
                baselineTotalBenefits,
                baselineTotalCosts,
                (benefits, costs, benefitsBaseline, costsBaseline) ->
                        (benefits - benefitsBaseline) - (costs - costsBaseline)
        );
    }

    private double paybackPeriod(
            List<Double> benefits,
            List<Double> baselineBenefits,
            List<Double> baselineCosts,
            List<Double> costs
    ) {
        var size = benefits.size();

        if (baselineBenefits.size() != size || baselineCosts.size() != size || costs.size() != size) {
            throw new IllegalStateException(
                    "Cannot find payback period of different length study periods. Given:\n\t" +
                            "Benefits\t\t\t" + benefits + "\n\t" +
                            "Baseline Benefits\t" + baselineBenefits + "\n\t" +
                            "Baseline Costs\t\t" + baselineCosts + "\n\t" +
                            "Costs\t\t\t\t" + costs + "\n"
            );
        }

        double accumulator = 0.0;
        for (int i = 0; i < size; i++) {
            accumulator += (benefits.get(i) - baselineBenefits.get(i)) - (baselineCosts.get(i) - costs.get(i));

            if (accumulator <= 0)
                return i;
        }

        return Double.POSITIVE_INFINITY;
    }

    private double bcr(
            double benefits,
            double benefitsBaseline,
            double costsInvest,
            double costsInvestBaseline,
            double costsNonInvest,
            double costsNonInvestBaseline
    ) {
        return checkFraction(
                (benefits - benefitsBaseline) - (costsNonInvest - costsNonInvestBaseline),
                costsInvest - costsInvestBaseline
        );
    }

    public Cell<Double> cTotalBenefits() {
        return cTotalBenefits;
    }

    public Cell<Double> cTotalCosts() {
        return cTotalCosts;
    }

    public Cell<Double> cTotalCostsInvest() {
        return cTotalCostsInvest;
    }

    public Cell<Double> cTotalCostsNonInvest() {
        return cTotalCostsNonInvest;
    }
}
