package gov.nist.eee.pipeline.edges;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.output.ResultNonSequenceOutputMapper;
import gov.nist.eee.output.ResultOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.measures.MeasureSummary;
import gov.nist.eee.pipeline.measures.MeasureSummaryPipeline;
import gov.nist.eee.pipeline.optional.OptionalCashflow;
import gov.nist.eee.pipeline.optional.OptionalCashflowPipeline;
import gov.nist.eee.pipeline.optional.OptionalKey;
import gov.nist.eee.pipeline.required.RequiredCashflow;
import gov.nist.eee.pipeline.required.RequiredCashflowPipeline;
import gov.nist.eee.tuple.Tuple2;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

import static gov.nist.eee.pipeline.edges.Tags.*;

@Pipeline(name = "edges", dependencies = {MeasureSummaryPipeline.class, RequiredCashflowPipeline.class, OptionalCashflowPipeline.class, EdgesBaselinePipeline.class})
@OutputMapper(ResultNonSequenceOutputMapper.class)
public class EdgesPipeline
        extends CellPipeline<Result<Map<Integer, EdgesSummary>, E3Exception>>
        implements IWithDependency {
    private static final Logger logger = LoggerFactory.getLogger(EdgesPipeline.class);
    private Cell<Integer> cHorizon;
    private Cell<Integer> cBaselineAlternative;
    private Cell<Result<Map<Integer, MeasureSummary>, E3Exception>> cMeasureSummaries;
    private Cell<Result<Map<Integer, RequiredCashflow>, E3Exception>> cRequired;
    private Cell<Result<Map<OptionalKey, OptionalCashflow>, E3Exception>> cOptional;
    private Cell<Result<Tuple2<EdgesSummary, EdgesBaselineValues>, E3Exception>> cEdgesBaseline;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up edges pipeline.");

        var sAnalysis = sInput.map(Input::analysis);
        cHorizon = sAnalysis.map(Analysis::studyPeriod).hold(25);
        cBaselineAlternative = sAnalysis.map(Analysis::baseAlternative).hold(0);
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for edges pipeline." + parameters);

        Cell<Result<Map<Integer, Cell<MeasureSummary>>, E3Exception>> cMeasureSummaries = parameters.get(MeasureSummaryPipeline.class);
        Cell<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>> cRequired = parameters.get(RequiredCashflowPipeline.class);
        Cell<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception>> cOptional = parameters.get(OptionalCashflowPipeline.class);
        this.cEdgesBaseline = parameters.get(EdgesBaselinePipeline.class);

        this.cMeasureSummaries = Cell.switchC(cMeasureSummaries.lift(cBaselineAlternative, (result, baselineAltID) -> result.on(
                measures -> CellUtils.sequenceMap(measures.entrySet()
                        .stream()
                        .filter(entry -> !entry.getKey().equals(baselineAltID))
                        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue))
                ).map(Result.Success::new),
                CellUtils::wrapError
        )));

        this.cRequired = Cell.switchC(cRequired.lift(cBaselineAlternative, (result, baselineAltID) -> result.on(
                required -> CellUtils.sequenceMap(required.entrySet()
                        .stream()
                        .filter(entry -> !entry.getKey().equals(baselineAltID))
                        .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue))
                ).map(Result.Success::new),
                CellUtils::wrapError
        )));

        this.cOptional = Cell.switchC(cOptional.lift(cBaselineAlternative, (result, baselineAltID) -> result.on(
                optionals -> {
                    var nonBaselineOptionals = new HashMap<OptionalKey, Cell<OptionalCashflow>>();

                    for (var entry : optionals.entrySet()) {
                        if (entry.getKey().altId() != baselineAltID)
                            nonBaselineOptionals.put(entry.getKey(), entry.getValue());
                    }

                    return CellUtils.sequenceMap(nonBaselineOptionals).map(Result.Success::new);
                },
                CellUtils::wrapError
        )));
    }

    @Override
    public Cell<Result<Map<Integer, EdgesSummary>, E3Exception>> define() {
        logger.trace("Defining edges pipeline.");

        return cMeasureSummaries.lift(cRequired, cOptional, cBaselineAlternative, cEdgesBaseline, cHorizon, (rMeasures, rRequired, rOptional, baselineAltID, rEdgesBaseline, horizon) ->
            rMeasures.flatMap(measures -> rRequired.flatMap(required -> rOptional.flatMap(optionals -> rEdgesBaseline.map(edgesBaseline -> {
                var result = new HashMap<Integer, EdgesSummary>();
                var baselineValues = edgesBaseline.e2();

                // Pass baseline summary to output
                result.put(baselineAltID, edgesBaseline.e1());

                var alternatives = measures.keySet();

                for (var altID : alternatives) {
                    var req = required.get(altID);
                    var measure = measures.get(altID);

                    var totalExternalDiscount = Util.elementwiseSubtract(req.totalBenefitsDiscountedExternal(), req.totalCostsDiscountedExternal());
                    var totalExt = Util.sum(totalExternalDiscount);

                    var tags = measure.totalTagFlows();
                    var otherTags = tags.entrySet()
                            .stream()
                            .filter(e -> !EDGES_TAGS.contains(e.getKey()))
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

                    var fatalitiesAverted = getFatalitiesAverted(altID, optionals);//Util.sum(optionals.get(new OptionalKey(altID, FATALITIES_AVERTED)).totalTagQuantity());

                    var npvDDisc = measure.totalTagFlows().getOrDefault(DRB, 0.0);
                    var npvInvestCosts = measure.totalCostsInvest();

                    var nbWdWeDisc = measure.netBenefits() != null ? measure.netBenefits() : 0.0;
                    var nbWdWoeDisc = nbWdWeDisc - (totalExt - baselineValues.external());
                    var nbWodWoeDisc = nbWdWoeDisc - (totalExt - baselineValues.external()) - (npvDDisc - baselineValues.npvDisasterDiscount());
                    var nbWodWeDisc = nbWdWeDisc - (npvDDisc - baselineValues.npvDisasterDiscount());

                    var investCosts = npvInvestCosts - baselineValues.npvInvestCosts();

                    var roiWdWe = annualizedROI(nbWdWeDisc, investCosts, horizon);
                    var roiWdWoe = annualizedROI(nbWdWoeDisc, investCosts, horizon);
                    var roiWodWe = annualizedROI(nbWodWeDisc, investCosts, horizon);
                    var roiWodWoe = annualizedROI(nbWodWoeDisc, investCosts, horizon);

                    var bcrWdWoe = MeasureSummaryPipeline.bcr(
                            measure.totalBenefits() - totalExt,
                            baselineValues.npvBenefits() - baselineValues.external(),
                            npvInvestCosts,
                            baselineValues.npvInvestCosts(),
                            measure.totalCostNonInvest(),
                            baselineValues.npvNonInvestCosts()
                    );

                    var diff1 = Util.elementwiseSubtract(req.totalBenefitsNonDiscounted(), totalExternalDiscount);
                    var baseDiff1 = Util.elementwiseSubtract(baselineValues.benefitsNonDiscounted(), baselineValues.externalNonDiscounted());

                    var i1 = Util.elementwiseSubtract(diff1, req.totalCostsNonDiscounted());
                    var i2 = Util.elementwiseSubtract(baseDiff1, baselineValues.costsNonDiscounted());

                    var irrWdWoe = MeasureSummaryPipeline.irr(Util.elementwiseSubtract(i1, i2));

                    result.put(altID, new EdgesSummary(
                            Util.sum(req.totalCostsDiscountedDirect()),
                            Util.sum(req.totalCostsDiscountedIndirect()),
                            tags.getOrDefault(OMR_RECURRING, 0.0),
                            tags.getOrDefault(OMR_ONE_TIME, 0.0),
                            tags.getOrDefault(POSITIVE_RECURRING, 0.0),
                            tags.getOrDefault(POSITIVE_ONE_TIME, 0.0),
                            tags.getOrDefault(NEGATIVE_RECURRING, 0.0),
                            tags.getOrDefault(NEGATIVE_ONE_TIME, 0.0),
                            measure.totalBenefits(),
                            measure.totalCosts(),
                            totalExt,
                            tags.getOrDefault(RESPONSE_AND_RECOVERY, 0.0),
                            tags.getOrDefault(DIRECT_LOSS_REDUCTION, 0.0),
                            tags.getOrDefault(INDIRECT_LOSS_REDUCTION, 0.0),
                            fatalitiesAverted,
                            tags.getOrDefault(FATALITIES_AVERTED, 0.0),
                            tags.getOrDefault(NDRB_RECURRING, 0.0),
                            tags.getOrDefault(NDRB_ONE_TIME, 0.0),
                            measure.netBenefits() != null ? measure.netBenefits() : 0.0,
                            measure.bcr() != null ? measure.bcr() : 0.0,
                            measure.irr() != null ? measure.irr() : 0.0,
                            roiWdWe,
                            roiWodWe,
                            nbWdWoeDisc,
                            bcrWdWoe,
                            irrWdWoe,
                            roiWdWoe,
                            roiWodWoe,
                            otherTags
                    ));
                }

                return result;
            }))))
        );
    }

    public static double annualizedROI(double netBenefit, double investCost, double horizon) {
        if (horizon == 0.0 || investCost == 0.0)
            return Double.NaN;

        return (netBenefit / investCost) * 100.0 * (1.0 / horizon);
    }

    private static double getFatalitiesAverted(int altID, Map<OptionalKey, OptionalCashflow> optionals) {
        var optional = optionals.get(new OptionalKey(altID, FATALITIES_AVERTED));

        if(optional == null)
            return 0.0;

        return Util.sum(optional.totalTagQuantity());
    }
}
