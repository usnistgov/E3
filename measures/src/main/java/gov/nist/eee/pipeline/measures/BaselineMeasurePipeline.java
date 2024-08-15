package gov.nist.eee.pipeline.measures;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.error.ErrorCode;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.optional.OptionalCashflow;
import gov.nist.eee.pipeline.optional.OptionalCashflowPipeline;
import gov.nist.eee.pipeline.optional.OptionalKey;
import gov.nist.eee.pipeline.required.RequiredCashflow;
import gov.nist.eee.pipeline.required.RequiredCashflowPipeline;
import gov.nist.eee.tuple.Tuple6;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

@Pipeline(name = "baseline-measure", dependencies = {OptionalCashflowPipeline.class, RequiredCashflowPipeline.class})
public class BaselineMeasurePipeline
        extends CellPipeline<Result<MeasureSummary, E3Exception>>
        implements IWithDependency {
    private static final Logger logger = LoggerFactory.getLogger(BaselineMeasurePipeline.class);
    private Cell<Double> cMarr;
    private Cell<Integer> cBaselineAltID;
    private Cell<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception>> cOptionalCashflows;
    private Cell<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>> cRequiredCashflows;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up baseline measure pipeline.");

        var sAnalysis = sInput.map(Input::analysis);
        cMarr = sAnalysis.map(Analysis::marr).hold(0.0);
        cBaselineAltID = sAnalysis.map(Analysis::baseAlternative).hold(0);
    }

    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for baseline measure pipeline." + parameters);

        cOptionalCashflows = parameters.get(OptionalCashflowPipeline.class);
        cRequiredCashflows = parameters.get(RequiredCashflowPipeline.class);
    }

    @Override
    public Cell<Result<MeasureSummary, E3Exception>> define() {
        logger.trace("Defining baseline measure pipeline.");

        return Cell.switchC(cRequiredCashflows.lift(
                cOptionalCashflows,
                cBaselineAltID,
                (rRequiredCashflows, rOptionalCashflows, baselineAltID) -> {
                    if (rOptionalCashflows instanceof Result.Failure<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception> failure) {
                        return new Cell<>(new Result.Failure<>(failure.error()));
                    } else if (rRequiredCashflows instanceof Result.Failure<Map<Integer, Cell<RequiredCashflow>>, E3Exception> failure) {
                        return new Cell<>(new Result.Failure<>(failure.error()));
                    } else if (rRequiredCashflows instanceof Result.Success<Map<Integer, Cell<RequiredCashflow>>, E3Exception> requiredCashflow &&
                            rOptionalCashflows instanceof Result.Success<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception> optionalCashflow) {
                        var x = requiredCashflow.value();
                        var y = optionalCashflow.value();

                        return defineBaselineSummary(x, y, baselineAltID).map(Result.Success::new);
                    }

                    return new Cell<>(new Result.Failure<>(new E3Exception(ErrorCode.E0000_UNREACHABLE, "Unreachable code path in baseline measure pipeline.")));
                }
        ));
    }

    private Cell<MeasureSummary> defineBaselineSummary(
            Map<Integer, Cell<RequiredCashflow>> required,
            Map<OptionalKey, Cell<OptionalCashflow>> optionals,
            Integer baselineAltID
    ) {
        var cRequiredCashflow = required.get(baselineAltID);
        var cOptionalCashflows = CellUtils.sequence(
                Util.group(optionals, key -> key.altId() == baselineAltID)
        );

        if (cRequiredCashflow == null)
            return new Cell<>(null);

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

        var cTotalTagFlows = cOptionalCashflows.map(
                Util.toMap(OptionalCashflow::tag, OptionalCashflow::totalTagCashflowDiscounted, Util::sum)
        );

        var cQuantitySum = cOptionalCashflows.map(
                Util.toMap(OptionalCashflow::tag, OptionalCashflow::totalTagQuantity, Util::sum)
        );

        var cQuantityUnits = cOptionalCashflows.map(
                Util.toMap(OptionalCashflow::tag, OptionalCashflow::units)
        );

        var combined = cTotalBenefitsDiscounted.lift(
                cTotalCosts,
                cTotalCostsInvest,
                cTotalCostsNonInvest,
                cTotalTagFlows,
                cQuantitySum,
                Tuple6::new
        );

        return combined.lift(cQuantityUnits, cMarr, (tuple, quantityUnits, marr) -> new MeasureSummary(
                baselineAltID,
                tuple.e1(),
                tuple.e2(),
                tuple.e3(),
                tuple.e4(),
                tuple.e5(),
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                tuple.e6(),
                quantityUnits,
                marr,
                null,
                null,
                null,
                null
        ));
    }
}
