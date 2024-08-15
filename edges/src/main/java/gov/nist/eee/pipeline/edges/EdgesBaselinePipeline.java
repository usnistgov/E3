package gov.nist.eee.pipeline.edges;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.error.ErrorCode;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.pipeline.CellPipeline;
import gov.nist.eee.pipeline.DependencyParameters;
import gov.nist.eee.pipeline.IWithDependency;
import gov.nist.eee.pipeline.Pipeline;
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

@Pipeline(name = "edges-baseline", dependencies = {MeasureSummaryPipeline.class, RequiredCashflowPipeline.class, OptionalCashflowPipeline.class})
public class EdgesBaselinePipeline
        extends CellPipeline<Result<Tuple2<EdgesSummary, EdgesBaselineValues>, E3Exception>>
        implements IWithDependency {
    private static final Logger logger = LoggerFactory.getLogger(EdgesPipeline.class);

    private Cell<Integer> cBaselineAlternative;
    private Cell<Result<MeasureSummary, E3Exception>> cBaselineMeasureSummary;
    private Cell<Result<RequiredCashflow, E3Exception>> cBaselineRequired;
    private Cell<Result<Map<String, OptionalCashflow>, E3Exception>> cBaselineOptionals;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up edges baseline pipeline.");

        var sAnalysis = sInput.map(Input::analysis);
        cBaselineAlternative = sAnalysis.map(Analysis::baseAlternative).hold(0);
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for edges baseline pipeline." + parameters);

        Cell<Result<Map<Integer, Cell<MeasureSummary>>, E3Exception>> cMeasureSummaries = parameters.get(MeasureSummaryPipeline.class);
        Cell<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>> cRequired = parameters.get(RequiredCashflowPipeline.class);
        Cell<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception>> cOptional = parameters.get(OptionalCashflowPipeline.class);

        // Get baseline measure summary
        this.cBaselineMeasureSummary = Cell.switchC(cMeasureSummaries.lift(cBaselineAlternative, (result, baselineAltID) -> result.on(
                measures -> {
                    var cMeasure = measures.get(baselineAltID);

                    if(cMeasure == null)
                        return new Cell<>(new Result.Failure<>(new E3Exception(ErrorCode.E0000_UNREACHABLE)));

                    return cMeasure.map(Result.Success::new);
                    },
                CellUtils::wrapError
        )));

        // Get baseline required object
        this.cBaselineRequired = Cell.switchC(cRequired.lift(cBaselineAlternative, (result, baselineAltID) -> result.on(
                required -> {
                    var cR = required.get(baselineAltID);

                    if(cR == null)
                        return new Cell<>(new Result.Failure<>(new E3Exception(ErrorCode.E0000_UNREACHABLE)));

                    return cR.map(Result.Success::new);
                },
                CellUtils::wrapError
        )));

        // Get optionals for baseline
        this.cBaselineOptionals = Cell.switchC(cOptional.lift(cBaselineAlternative, (result, baselineAltID) -> result.on(
                optionals -> {
                    var filtered = filterOptionalCashflowsByAltID(baselineAltID, optionals);
                    return CellUtils.sequenceMap(filtered).map(Result.Success::new);
                },
                CellUtils::wrapError
        )));

    }

    @Override
    public Cell<Result<Tuple2<EdgesSummary, EdgesBaselineValues>, E3Exception>> define() {
        logger.trace("Defining edges baseline pipeline.");

        return cBaselineMeasureSummary.lift(cBaselineRequired, cBaselineOptionals, (rMeasure, rRequired, rOptional) ->
                rMeasure.flatMap(measure -> rRequired.flatMap(required -> rOptional.map(optionals -> {
                    var cFatalitiesAvertedOptional = optionals.get(FATALITIES_AVERTED);

                    var baselineCostNonDisc = required.totalCostsNonDiscounted();
                    var baselineBensNonDisc = required.totalBenefitsNonDiscounted();
                    var baselineExtDisc = Util.elementwiseSubtract(required.totalBenefitsDiscountedExternal(), required.totalCostsDiscountedExternal());
                    var baselineExtNonDisc = Util.elementwiseSubtract(required.totalBenefitsNonDiscountedExternal(), required.totalCostsNonDiscountedExternal());

                    var baselineFatilityAverted = cFatalitiesAvertedOptional != null ? Util.sum(cFatalitiesAvertedOptional.totalTagQuantity()) : 0.0;

                    var baselineNpvDisasterDiscount = measure.totalTagFlows().getOrDefault(DRB, 0.0);
                    var baselineNpvInvestCosts = measure.totalCostsInvest();
                    var baselineNpvBenefits = measure.totalBenefits();
                    var baselineNpvNonInvestCosts = measure.totalCostNonInvest();
                    var baselineExternal = Util.sum(baselineExtDisc);

                    var tags = measure.totalTagFlows();
                    var otherTags = tags.entrySet()
                            .stream()
                            .filter(e -> !EDGES_TAGS.contains(e.getKey()))
                            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

                    var baselineValues = new EdgesBaselineValues(
                            baselineCostNonDisc,
                            baselineBensNonDisc,
                            baselineExtNonDisc,
                            baselineNpvInvestCosts,
                            baselineNpvBenefits,
                            baselineNpvNonInvestCosts,
                            baselineExternal,
                            baselineNpvDisasterDiscount
                    );

                    var summary = new EdgesSummary(
                            Util.sum(required.totalCostsDiscountedDirect()),
                            Util.sum(required.totalCostsDiscountedIndirect()),
                            tags.getOrDefault(OMR_RECURRING, 0.0),
                            tags.getOrDefault(OMR_ONE_TIME, 0.0),
                            tags.getOrDefault(POSITIVE_RECURRING, 0.0),
                            tags.getOrDefault(POSITIVE_ONE_TIME, 0.0),
                            tags.getOrDefault(NEGATIVE_RECURRING, 0.0),
                            tags.getOrDefault(NEGATIVE_ONE_TIME, 0.0),
                            measure.totalBenefits(),
                            measure.totalCosts(),
                            baselineExternal,
                            tags.getOrDefault(RESPONSE_AND_RECOVERY, 0.0),
                            tags.getOrDefault(DIRECT_LOSS_REDUCTION, 0.0),
                            tags.getOrDefault(INDIRECT_LOSS_REDUCTION, 0.0),
                            baselineFatilityAverted,
                            tags.getOrDefault(FATALITIES_AVERTED, 0.0),
                            tags.getOrDefault(NDRB_RECURRING, 0.0),
                            tags.getOrDefault(NDRB_ONE_TIME, 0.0),
                            measure.netBenefits() != null ? measure.netBenefits() : 0.0,
                            measure.bcr() != null ? measure.bcr() : 0.0,
                            measure.irr() != null ? measure.irr() : 0.0,
                            0.0,
                            0.0,
                            0.0,
                            Double.NaN,
                            100.0,
                            Double.NaN,
                            Double.NaN,
                            otherTags
                    );

                    return new Tuple2<>(summary, baselineValues);
                }))));
    }

    public static Map<String, Cell<OptionalCashflow>> filterOptionalCashflowsByAltID(
            int id, Map<OptionalKey, Cell<OptionalCashflow>> optionals
    ) {
        var result = new HashMap<String, Cell<OptionalCashflow>>();

        for (var entry : optionals.entrySet()) {
            if (entry.getKey().altId() == id)
                result.put(entry.getKey().tag(), entry.getValue());
        }

        return result;
    }
}
