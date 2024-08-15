package gov.nist.eee.pipeline.measures;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.object.input.TimestepComp;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.discounted.DiscountedPipeline;
import gov.nist.eee.pipeline.discounted.presentvalue.PresentValueFormula;
import gov.nist.eee.pipeline.optional.OptionalCashflow;
import gov.nist.eee.pipeline.optional.OptionalCashflowPipeline;
import gov.nist.eee.pipeline.optional.OptionalKey;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.pipeline.required.RequiredCashflow;
import gov.nist.eee.pipeline.required.RequiredCashflowPipeline;
import gov.nist.eee.tuple.Tuple3;
import gov.nist.eee.tuple.Tuple6;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import org.apache.commons.math3.analysis.solvers.RiddersSolver;
import org.apache.commons.math3.exception.NoBracketingException;
import org.apache.commons.math3.util.FastMath;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

import static gov.nist.eee.util.Util.*;

@Pipeline(name = "measure", dependencies = {BaselineMeasurePipeline.class, OptionalCashflowPipeline.class, RequiredCashflowPipeline.class}, inputDependencies = {QuantityPipeline.class})
@OutputMapper(MeasureOutputMapper.class)
public class MeasureSummaryPipeline
        extends CellPipeline<Result<Map<Integer, Cell<MeasureSummary>>, E3Exception>>
        implements IWithDependency, IWithInput {
    private static final Logger logger = LoggerFactory.getLogger(MeasureSummaryPipeline.class);
    private Cell<Integer> cStudyPeriod;
    private Cell<Double> cMarr;
    private Cell<Double> cReinvestRate;
    private Cell<Integer> cBaselineAltID;
    private Cell<Double> cDiscountRate;
    private Cell<TimestepComp> cTimestepComp;
    private Cell<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception>> cOptionalCashflows;
    private Cell<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>> cRequiredCashflows;
    private Cell<Result<MeasureSummary, E3Exception>> cBaselineSummary;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up measure pipeline.");

        var sAnalysis = sInput.map(Input::analysis);
        cMarr = sAnalysis.map(Analysis::marr).hold(0.0);
        cReinvestRate = sAnalysis.map(Analysis::reinvestRate).hold(0.06);
        cBaselineAltID = sAnalysis.map(Analysis::baseAlternative).hold(0);
        cDiscountRate = sAnalysis.map(Analysis::discountRateReal).hold(0.0);
        cTimestepComp = sAnalysis.map(Analysis::timestepComp).hold(TimestepComp.END_OF_YEAR);
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for measure pipeline." + parameters);

        cOptionalCashflows = parameters.get(OptionalCashflowPipeline.class);
        cRequiredCashflows = parameters.get(RequiredCashflowPipeline.class);
        cBaselineSummary = parameters.get(BaselineMeasurePipeline.class);
    }

    @Override
    public void setupInput(Cell<Model> cModel) {
        logger.trace("Setting up input for measure summary pipeline");

        cStudyPeriod = Cell.switchC(cModel.map(model ->
                model.intInputs().get(new String[]{"analysisObject", "studyPeriod"})
        ));
    }

    @Override
    public Cell<Result<Map<Integer, Cell<MeasureSummary>>, E3Exception>> define() {
        logger.trace("Defining measure pipeline.");

        return cRequiredCashflows.lift(
                cOptionalCashflows,
                cBaselineAltID,
                cBaselineSummary,
                (rRequiredCashflows, rOptionalCashflows, baselineAltID, rBaselineSummary) ->
                        rRequiredCashflows.flatMap(requiredCashflows ->
                                rOptionalCashflows.flatMap(optionalCashflows ->
                                        rBaselineSummary.map(baselineSummary -> {
                                                    var result = baselineSummary != null ? defineMeasureSummaryCells(
                                                            requiredCashflows,
                                                            optionalCashflows,
                                                            baselineAltID,
                                                            baselineSummary
                                                    ) : new HashMap<Integer, Cell<MeasureSummary>>(1);

                                                    // Pass baseline measure through to final results.
                                                    result.put(baselineAltID, new Cell<>(baselineSummary));

                                                    return result;
                                                }
                                        )
                                )
                        )
        );
    }

    private Cell<Tuple6<Integer, Double, Double, Double, Double, Map<String, Double>>> getPartOne(
            int altID,
            Cell<RequiredCashflow> cRequiredCashflow,
            Cell<List<OptionalCashflow>> cOptionalCashflows
    ) {
        var cTotalBenefitsDiscounted = cRequiredCashflow
                .map(RequiredCashflow::totalBenefitsDiscounted)
                .map(Util::sum);

        var cTotalCosts = cRequiredCashflow
                .map(RequiredCashflow::totalCostsDiscounted)
                .map(Util::sum);

        var cTotalCostsInvest = cRequiredCashflow
                .map(RequiredCashflow::totalCostsDiscountedInvest)
                .map(Util::sum);

        var cTotalCostsNonInvest = cRequiredCashflow
                .map(RequiredCashflow::totalCostsDiscountedNonInvest)
                .map(Util::sum);

        var cTotalTagFlows = cOptionalCashflows
                .map(
                        Util.toMap(OptionalCashflow::tag, OptionalCashflow::totalTagCashflowDiscounted, Util::sum)
                );

        return new Cell<>(altID).lift(
                cTotalBenefitsDiscounted,
                cTotalCosts,
                cTotalCostsInvest,
                cTotalCostsNonInvest,
                cTotalTagFlows,
                Tuple6::new
        );
    }

    private Cell<Tuple6<Double, Double, Double, Double, Double, Double>> getPartTwo(
            Cell<Tuple6<Integer, Double, Double, Double, Double, Map<String, Double>>> partOne,
            Cell<RequiredCashflow> cRequiredCashflow,
            MeasureSummary baseline,
            Cell<RequiredCashflow> cBaselineRequiredCashflow
    ) {
        var cTotalNonDiscounted = cRequiredCashflow
                .map(RequiredCashflow::totalBenefitsNonDiscounted)
                .lift(
                        cRequiredCashflow.map(RequiredCashflow::totalCostsNonDiscounted),
                        Util::elementwiseSubtract
                );
        var cBaselineTotalNonDiscounted = cBaselineRequiredCashflow
                .map(RequiredCashflow::totalBenefitsNonDiscounted)
                .lift(
                        cBaselineRequiredCashflow.map(RequiredCashflow::totalCostsNonDiscounted),
                        Util::elementwiseSubtract
                );
        var cTotalBenefitsDiscounted = partOne.map(Tuple6::e2);
        var cTotalCosts = partOne.map(Tuple6::e3);
        var cTotalCostsInvest = partOne.map(Tuple6::e4);
        var cTotalCostsNonInvest = partOne.map(Tuple6::e5);
        var baselineTotalBenefits = baseline == null ? 0.0 : baseline.totalBenefits();
        var baselineTotalCosts = baseline == null ? 0.0 : baseline.totalCosts();
        var baselineCostsNonInvest = baseline == null ? 0.0 : baseline.totalCostNonInvest();
        var baselineCostsInvest = baseline == null ? 0.0 : baseline.totalCostsInvest();

        var cNetBenefits = netBenefits(
                cTotalBenefitsDiscounted, cTotalCosts, baselineTotalBenefits, baselineTotalCosts
        );

        var cNetSavings = netSavings(cTotalCosts, baselineTotalCosts);

        var cSir = sir(
                cTotalCostsNonInvest, cTotalCostsInvest, baselineCostsNonInvest, baselineCostsInvest
        );

        var cIrr = cBaselineTotalNonDiscounted.lift(
                cTotalNonDiscounted, MeasureSummaryPipeline::calculateIrr
        );

        var cAirrParameters = cReinvestRate.lift(cStudyPeriod, cDiscountRate, cNetBenefits, cTotalCostsInvest, cTimestepComp, Tuple6::new);
        var cAirr = cAirrParameters.lift(cBaselineRequiredCashflow, cRequiredCashflow,
                (parameters, base, flow) -> airr(
                        parameters.e1(), parameters.e2(), parameters.e3(),
                        parameters.e4(), parameters.e5(), baselineCostsInvest,
                        parameters.e6(), base, flow
                )
        );

        var cDpp = cRequiredCashflow.lift(cBaselineRequiredCashflow, this::calculateDpp);

        return cNetBenefits.lift(
                cNetSavings,
                cSir,
                cIrr,
                cAirr,
                cDpp,
                Tuple6::new
        );
    }

    private Cell<Tuple6<Double, Double, Map<String, Double>, Map<String, String>, Double, Map<String, Double>>> getPartThree(
            Cell<Tuple6<Integer, Double, Double, Double, Double, Map<String, Double>>> partOne,
            Cell<RequiredCashflow> cRequiredCashflow,
            MeasureSummary baseline,
            Cell<RequiredCashflow> cBaselineRequiredCashflow,
            Cell<List<OptionalCashflow>> cOptionalCashflows,
            Cell<Double> cMarr
    ) {
        var cTotalBenefitsDiscounted = partOne.map(Tuple6::e2);
        var cTotalCostsInvest = partOne.map(Tuple6::e4);
        var cTotalCostsNonInvest = partOne.map(Tuple6::e5);
        var baselineCostsInvest = baseline == null ? 0.0 : baseline.totalCostsInvest();
        var baselineCostsNonInvest = baseline == null ? 0.0 : baseline.totalCostNonInvest();
        var baselineTotalBenefits = baseline == null ? 0.0 : baseline.totalBenefits();

        var cSpp = cRequiredCashflow.lift(cBaselineRequiredCashflow, this::calculateSpp);

        var cBcr = cTotalBenefitsDiscounted.lift(
                cTotalCostsInvest,
                cTotalCostsNonInvest,
                (totalBenefitsDiscounted, totalCostsInvest, totalCostsNonInvest) -> calculateBcr(
                        totalBenefitsDiscounted,
                        totalCostsInvest,
                        totalCostsNonInvest,
                        baselineCostsInvest,
                        baselineCostsNonInvest,
                        baselineTotalBenefits
                )
        );

        var cQuantitySum = cOptionalCashflows.map(
                Util.toMap(OptionalCashflow::tag, OptionalCashflow::totalTagQuantity, Util::sum)
        );

        var cQuantityUnits = cOptionalCashflows.map(
                Util.toMap(OptionalCashflow::tag, OptionalCashflow::units)
        );

        var baselineQuantitySum = baseline == null ? new HashMap<String, Double>() : baseline.quantitySum();
        var cDeltaQuantity = deltaQuantity(cOptionalCashflows, baselineQuantitySum);

        return cSpp.lift(
                cBcr,
                cQuantitySum,
                cQuantityUnits,
                cMarr,
                cDeltaQuantity,
                Tuple6::new
        );
    }

    private Cell<Tuple3<Map<String, Double>, Map<String, Double>, Map<String, Double>>> getPartFour(
            Cell<Double> cNetSavings,
            Cell<Double> cTotalCosts,
            MeasureSummary baseline,
            Cell<List<OptionalCashflow>> cOptionalCashflows
    ) {
        var baselineQuantitySums = baseline == null ? new HashMap<String, Double>() : baseline.quantitySum();

        var cNsPercentQuantity = cNetSavings.lift(
                cOptionalCashflows,
                (netSavings, optionalCashflows) ->
                        calculateNsPercentQuantity(netSavings, optionalCashflows, baselineQuantitySums)
        );

        var baselineDeltaQuantity = baseline == null ? new HashMap<String, Double>() : baseline.deltaQuantity();

        var cNsDeltaQuantity = cNetSavings.lift(
                cOptionalCashflows,
                (netSavings, optionalCashflows) ->
                        calculateNsDeltaQuantity(netSavings, optionalCashflows, baselineDeltaQuantity)
        );

        var cNsElasticityQuantity = cNetSavings.lift(
                cTotalCosts,
                cOptionalCashflows,
                (netSavings, totalCosts, optionalCashflows) ->
                        calculateNsElasticityQuantity(netSavings, totalCosts, optionalCashflows, baselineQuantitySums)
        );

        return cNsPercentQuantity.lift(
                cNsDeltaQuantity,
                cNsElasticityQuantity,
                Tuple3::new
        );
    }

    private Cell<Double> netBenefits(
            Cell<Double> totalBenefits,
            Cell<Double> totalCosts,
            double baselineTotalBenefits,
            double baselineTotalCosts
    ) {
        return totalBenefits.lift(
                totalCosts,
                (benefits, costs) -> MeasureSummaryPipeline.calculateTotalBenefits(benefits, costs, baselineTotalBenefits, baselineTotalCosts)
        );
    }

    private Cell<Double> netSavings(Cell<Double> costs, double baselineCosts) {
        return costs.map(cost -> MeasureSummaryPipeline.calculateNetSavings(baselineCosts, cost));
    }

    private Cell<Double> sir(Cell<Double> costsNonInvest, Cell<Double> costsInvest, double costsNonInvestBaseline, double costsInvestBaseline) {
        return costsNonInvest.lift(
                costsInvest,
                (a, b) -> checkFraction(costsNonInvestBaseline - a, b - costsInvestBaseline)
        );
    }

    private static Double checkFraction(Double numerator, Double denominator) {
        if (denominator <= 0 && numerator > 0)
            return Double.POSITIVE_INFINITY;
        else if (denominator <= 0 && numerator <= 0)
            return Double.NaN;
        else
            return numerator / denominator;
    }

    private List<Double> terminalValueArray(int size, TimestepComp compounding, double rate) {
        var result = new ArrayList<Double>(size);

        for (var i = 0; i < size; i++) {
            if (compounding == TimestepComp.END_OF_YEAR || (compounding == TimestepComp.MID_YEAR && i == 0))
                result.add(Math.pow(1.0 + rate, size - 1.0 - i));
            else if (compounding == TimestepComp.MID_YEAR)
                result.add(Math.pow(1.0 + rate, size - 1.0 - i + 0.5));
            else if (compounding == TimestepComp.CONTINUOUS)
                result.add(Math.exp(rate * (size - 1.0 - i)));
        }

        return result;
    }

    private double airr(
            double reinvestRate, int studyPeriod, double discountRate, double netBenefits,
            double totCostsInv, double totCostsInvBase, TimestepComp timestepComp,
            RequiredCashflow baseline, RequiredCashflow flow
    ) {

        var discountingFunction = DiscountedPipeline.getPresentValueFormula(timestepComp);

        if (timestepComp == TimestepComp.CONTINUOUS)
            return compoundingAirr(reinvestRate, studyPeriod, timestepComp, baseline, flow, discountingFunction);

        if (Math.abs(reinvestRate - discountRate) <= 0.000001) {
            var fraction = checkFraction(netBenefits, totCostsInv - totCostsInvBase);

            if (fraction == null || fraction.isNaN() || fraction.isInfinite() || fraction <= 0.0)
                return Double.NaN;

            return (1.0 + reinvestRate) * Math.pow((1.0 + fraction), 1.0 / studyPeriod) - 1.0;
        }

        return defaultAirr(reinvestRate, studyPeriod, baseline, flow, discountingFunction);
    }

    private static double defaultAirr(
            double reinvestRate, int studyPeriod, RequiredCashflow baseline,
            RequiredCashflow flow, PresentValueFormula discountingFunction
    ) {
        var invDiff = elementwiseSubtract(flow.totalCostsNonDiscountedInvest(), baseline.totalCostsNonDiscountedInvest());
        var presValInv = sum(DiscountedPipeline.discountValues(invDiff, reinvestRate, discountingFunction));

        var altNetBenNonDisc = elementwiseSubtract(flow.totalBenefitsNonDiscounted(), flow.totalCostsNonDiscounted());
        var baseNetBenNonDisc = elementwiseSubtract(baseline.totalBenefitsNonDiscounted(), baseline.totalCostsNonDiscounted());
        var netBenNonDisc = elementwiseSubtract(altNetBenNonDisc, baseNetBenNonDisc);
        var presValNetBen = sum(DiscountedPipeline.discountValues(netBenNonDisc, reinvestRate, discountingFunction));

        var fraction = checkFraction(presValNetBen, presValInv);

        return (1.0 + reinvestRate) * Math.pow(1.0 + fraction, 1.0 / studyPeriod) - 1.0;
    }

    private double compoundingAirr(
            double reinvestRate, int studyPeriod, TimestepComp timestepComp,
            RequiredCashflow baseline, RequiredCashflow flow, PresentValueFormula discountingFunction
    ) {
        var invDiff = elementwiseSubtract(flow.totalCostsNonDiscountedInvest(), baseline.totalCostsNonDiscountedInvest());
        var presValInv = sum(DiscountedPipeline.discountValues(invDiff, reinvestRate, discountingFunction));

        var altTermValNonDisc = elementwiseSubtract(flow.totalBenefitsNonDiscounted(), flow.totalCostsNonDiscountedNonInvest());
        var baseTermValNonDisc = elementwiseSubtract(baseline.totalBenefitsNonDiscounted(), baseline.totalCostsNonDiscountedNonInvest());
        var termValNonDisc = elementwiseSubtract(altTermValNonDisc, baseTermValNonDisc);
        var termValDisc = sum(elementwiseMultiply(
                termValNonDisc, terminalValueArray(termValNonDisc.size(), timestepComp, reinvestRate)
        ));

        var fraction = checkFraction(termValDisc, presValInv);

        if (fraction == null || fraction.isNaN() || fraction.isInfinite() || fraction <= 0.0)
            return Double.NaN;

        return Math.log(fraction) * 1 / studyPeriod;
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
            accumulator += (costs.get(i) - baselineCosts.get(i)) + (baselineBenefits.get(i) - benefits.get(i));

            if (accumulator <= 0)
                return i;
        }

        return Double.POSITIVE_INFINITY;
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
            var sum = sum(optional.totalTagQuantity());

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
            var quantitySum = sum(optional.totalTagQuantity());

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
            Cell<List<OptionalCashflow>> cOptionals,
            Map<String, Double> baselineQuantitySum
    ) {
        return cOptionals.map((optionals) -> {
            var result = new HashMap<String, Double>();

            for (var optional : optionals) {
                var tag = optional.tag();
                var quantitySum = sum(optional.totalTagQuantity());

                result.put(optional.tag(), quantitySum - baselineQuantitySum.getOrDefault(tag, 0.0));
            }

            return result;
        });
    }

    public static double bcr(
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

    public static double irr(List<Double> values) {
        return irr(values, 0.0001);
    }

    public static double irr(List<Double> values, double tolerance) {
        var ridders = new RiddersSolver(tolerance);

        var result = ridders.solve(100, (double r) -> sumIrr(values, r), -0.0, 10.0);
        if (!Double.isNaN(result))
            return result;

        return ridders.solve(100, (double r) -> sumIrr(values, r), -10.0, 0.0);
    }

    public static double sumIrr(List<Double> values, double r) {
        var sum = 0.0;
        for (int i = 0; i < values.size(); i++) {
            sum += values.get(i) / FastMath.pow(1 + r, i);
        }
        return sum;
    }

    private Map<Integer, Cell<MeasureSummary>> defineMeasureSummaryCells(
            Map<Integer, Cell<RequiredCashflow>> required,
            Map<OptionalKey, Cell<OptionalCashflow>> optionals,
            Integer baselineAltID,
            MeasureSummary baselineSummary
    ) {
        var result = new HashMap<Integer, Cell<MeasureSummary>>();
        var cBaselineRequiredCashflow = Cell.switchC(cBaselineAltID.map(required::get));

        for (var entry : required.entrySet()) {
            var altID = entry.getKey();

            // Ignore baseline alternative since it has already been calculated
            if (Objects.equals(altID, baselineAltID))
                continue;

            var cRequiredCashflow = entry.getValue();
            var cOptionalCashflows = CellUtils.sequence(
                    Util.group(optionals, key -> key.altId() == altID)
            );

            if (cRequiredCashflow == null)
                continue;

            // Create measure summary parts. Necessary because of limitation on Cell lifting.
            var partOne = getPartOne(altID, cRequiredCashflow, cOptionalCashflows);
            var partTwo = getPartTwo(partOne, cRequiredCashflow, baselineSummary, cBaselineRequiredCashflow);
            var partThree = getPartThree(partOne, cRequiredCashflow, baselineSummary, cBaselineRequiredCashflow, cOptionalCashflows, cMarr);
            var partFour = getPartFour(partTwo.map(Tuple6::e2), partOne.map(Tuple6::e3), baselineSummary, cOptionalCashflows);

            // Combine parts into measure summary
            var cMeasureSummary = partOne.lift(
                    partTwo, partThree, partFour, MeasureSummaryPipeline::combineSummaryParts
            );

            result.put(altID, cMeasureSummary);
        }

        return result;
    }

    private static Double calculateIrr(List<Double> baselineTotal, List<Double> total) {
        var values = elementwiseSubtract(total, baselineTotal);

        try {
            return irr(values);
        } catch (NoBracketingException e) {
            logger.warn("No bracketing exception! " + e);
            return null;
        }
    }

    private Double calculateDpp(RequiredCashflow requiredFlow, RequiredCashflow baselineFlow) {
        if (baselineFlow == null)
            return null;

        return paybackPeriod(
                requiredFlow.totalBenefitsDiscounted(),
                baselineFlow.totalBenefitsDiscounted(),
                baselineFlow.totalCostsDiscounted(),
                requiredFlow.totalCostsDiscounted()
        );
    }

    private Double calculateSpp(RequiredCashflow requiredFlow, RequiredCashflow baselineFlow) {
        if (baselineFlow == null)
            return null;

        return paybackPeriod(
                requiredFlow.totalBenefitsNonDiscounted(),
                baselineFlow.totalBenefitsNonDiscounted(),
                baselineFlow.totalCostsNonDiscounted(),
                requiredFlow.totalCostsNonDiscounted()
        );
    }

    private Double calculateBcr(
            Double netBenefits,
            Double totalCostsInvest,
            Double totalCostsNonInvest,
            double totalCostsInvestBaseline,
            double totalCostsNonInvestBaseline,
            double netBenefitsBaseline
    ) {
        if (netBenefits == null)
            return null;

        return bcr(netBenefits, netBenefitsBaseline, totalCostsInvest, totalCostsInvestBaseline, totalCostsNonInvest, totalCostsNonInvestBaseline);
    }

    private Map<String, Double> calculateNsPercentQuantity(
            Double netSavings,
            List<OptionalCashflow> optionalCashflows,
            Map<String, Double> baseSums
    ) {
        if (baseSums == null)
            return null;

        return nsPercentQuantity(netSavings, optionalCashflows, baseSums);
    }

    private Map<String, Double> calculateNsDeltaQuantity(Double netSavings, List<OptionalCashflow> optionalCashflows, Map<String, Double> baseDeltaQuantity) {
        if (baseDeltaQuantity == null)
            return null;

        return nsDeltaQuantity(netSavings, optionalCashflows, baseDeltaQuantity);
    }

    private Map<String, Double> calculateNsElasticityQuantity(Double netSavings, Double totalCosts, List<OptionalCashflow> optionalCashflows, Map<String, Double> baseQuantitySum) {
        if (netSavings == null || baseQuantitySum == null)
            return null;

        return nsElasticityQuantity(netSavings, totalCosts, optionalCashflows, baseQuantitySum);
    }

    private static Double calculateNetSavings(Double bc, Double c) {
        return bc - c;
    }

    private static Double calculateTotalBenefits(Double benefits, Double costs, Double benefitsBaseline, Double costsBaseline) {
        return (benefits - benefitsBaseline) - (costs - costsBaseline);
    }

    private static MeasureSummary combineSummaryParts(Tuple6<Integer, Double, Double, Double, Double, Map<String, Double>> p1, Tuple6<Double, Double, Double, Double, Double, Double> p2, Tuple6<Double, Double, Map<String, Double>, Map<String, String>, Double, Map<String, Double>> p3, Tuple3<Map<String, Double>, Map<String, Double>, Map<String, Double>> p4) {
        return new MeasureSummary(
                p1.e1(), p1.e2(), p1.e3(), p1.e4(), p1.e5(), p1.e6(), p2.e1(),
                p2.e2(), p2.e3(), p2.e4(), p2.e5(), p2.e6(), p3.e1(), p3.e2(),
                p3.e3(), p3.e4(), p3.e5(), p3.e6(), p4.e1(), p4.e2(), p4.e3()
        );
    }
}
