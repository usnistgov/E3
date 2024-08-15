package gov.nist.eee.pipeline.required;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.*;
import gov.nist.eee.output.ResultOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.discounted.DiscountedPipeline;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.pipeline.residualvalue.ResidualValuePipeline;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

@Pipeline(name = "required", dependencies = {DiscountedPipeline.class, ResidualValuePipeline.class}, inputDependencies = {QuantityPipeline.class})
@OutputMapper(RequiredOutputMapper.class)
public class RequiredCashflowPipeline
        extends CellPipeline<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>>
        implements IWithDependency, IWithInput {
    private static final Logger logger = LoggerFactory.getLogger(RequiredCashflowPipeline.class);

    private Cell<Integer> cStudyPeriod;
    private Cell<Map<Integer, Bcn>> cBcns;
    private Cell<Map<Integer, Set<Integer>>> cBcnAltIDs;
    private Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> cResidualValues;
    private Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>> cDiscounted;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up required cashflow pipeline.");

        cBcns = Util.toMap(sInput.map(Input::bcnObjects).hold(List.of()), Bcn::id, x -> x);
        cBcnAltIDs = sInput.map(Input::alternativeObjects).hold(List.of()).map(Util::groupByBcn);
    }



    @Override
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for required cashflow pipeline. " + parameters);

        cResidualValues = parameters.get(ResidualValuePipeline.class);
        cDiscounted = parameters.get(DiscountedPipeline.class);
    }

    @Override
    public void setupInput(Cell<Model> cModel) {
        logger.trace("Setting up input for required cashflow pipeline. " + cModel);

        cStudyPeriod = Cell.switchC(cModel.map(model ->
                model.intInputs().get(new String[]{"analysisObject", "studyPeriod"})
        ));
    }

    @Override
    public Cell<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>> define() {
        logger.trace("Defining required cashflow pipeline.");

        return cBcns.lift(
                cDiscounted,
                cResidualValues,
                cStudyPeriod,
                cBcnAltIDs,
                (bcns, rdiscounted, rresidualValues, studyPeriod, altIDs) -> rdiscounted.flatMap(discounted -> rresidualValues.map(residualValues -> {

                    var cache = new HashMap<Integer, List<Cell<NormalizedRequiredCashflow>>>();

                    for (var entry : bcns.entrySet()) {
                        var bcnID = entry.getKey();
                        var bcn = entry.getValue();

                        var cDiscountedValues = discounted.get(bcnID);
                        var cValues = residualValues.get(bcnID);


                        var cDiscountedIntermediate = createIntermediateCashflow(bcn, cDiscountedValues, studyPeriod);
                        var cResiudalValueIntermediate = createIntermediateCashflow(bcn, cValues, studyPeriod);

                        var cRequiredCashflow = combineIntermediateCashflows(isCost(bcn), isBenefit(bcn), cDiscountedIntermediate, cResiudalValueIntermediate);

                        for (var altID : altIDs.get(bcnID)) {
                            cache.computeIfAbsent(altID, ArrayList::new).add(cRequiredCashflow);
                        }
                    }

                    var result = new HashMap<Integer, Cell<RequiredCashflow>>();

                    for (var entry : cache.entrySet()) {
                        var altID = entry.getKey();
                        var cashflows = entry.getValue();

                        var cCombinedCashflow = CellUtils.mergeList(NormalizedRequiredCashflow::add, cashflows);
                        result.put(altID, cCombinedCashflow.map(cashflow -> new RequiredCashflow(altID, cashflow)));
                    }

                    return result;
                }))
        );
    }

    private Cell<IntermediateCashflow> createIntermediateCashflow(
            Bcn bcn,
            Cell<List<Double>> cValues,
            int studyPeriod
    ) {
        var defaultArray = new ArrayList<Double>(studyPeriod + 1);
        for (int i = 0; i < studyPeriod + 1; i++) {
            defaultArray.add(0.0);
        }

        return cValues.map(values -> new IntermediateCashflow(
                values,
                isInvest(bcn) ? values : defaultArray,
                isNonInvest(bcn) ? values : defaultArray,
                isDirect(bcn) ? values : defaultArray,
                isIndirect(bcn) ? values : defaultArray,
                isExternality(bcn) ? values : defaultArray
        ));
    }

    private Cell<NormalizedRequiredCashflow> combineIntermediateCashflows(
            boolean isCost,
            boolean isBenefit,
            Cell<IntermediateCashflow> cDiscounted,
            Cell<IntermediateCashflow> cNonDiscounted
    ) {
        return cDiscounted.lift(
                cNonDiscounted,
                (discounted, nonDiscounted) -> {
                    var defaultArray = new ArrayList<Double>(discounted.general().size());
                    for (int i = 0; i < discounted.general().size(); i++) {
                        defaultArray.add(0.0);
                    }

                    return new NormalizedRequiredCashflow(
                            isCost ? nonDiscounted.general() : defaultArray,
                            isCost ? discounted.general() : defaultArray,
                            isBenefit ? nonDiscounted.general() : defaultArray,
                            isBenefit ? discounted.general() : defaultArray,

                            isCost ? nonDiscounted.invest() : defaultArray,
                            isCost ? discounted.invest() : defaultArray,
                            isBenefit ? nonDiscounted.invest() : defaultArray,
                            isBenefit ? discounted.invest() : defaultArray,

                            isCost ? nonDiscounted.nonInvest() : defaultArray,
                            isCost ? discounted.nonInvest() : defaultArray,
                            isBenefit ? nonDiscounted.nonInvest() : defaultArray,
                            isBenefit ? discounted.nonInvest() : defaultArray,

                            isCost ? nonDiscounted.direct() : defaultArray,
                            isCost ? discounted.direct() : defaultArray,
                            isBenefit ? nonDiscounted.direct() : defaultArray,
                            isBenefit ? discounted.direct() : defaultArray,

                            isCost ? nonDiscounted.indirect() : defaultArray,
                            isCost ? discounted.indirect() : defaultArray,
                            isBenefit ? nonDiscounted.indirect() : defaultArray,
                            isBenefit ? discounted.indirect() : defaultArray,

                            isCost ? nonDiscounted.externality() : defaultArray,
                            isCost ? discounted.externality() : defaultArray,
                            isBenefit ? nonDiscounted.externality() : defaultArray,
                            isBenefit ? discounted.externality() : defaultArray

                    );
                }
        );
    }

    private static boolean isCost(Bcn bcn) {
        return bcn.type() == BcnType.COST;
    }

    private static boolean isBenefit(Bcn bcn) {
        return bcn.type() == BcnType.BENEFIT;
    }

    private static boolean isInvest(Bcn bcn) {
        return bcn.invest();
    }

    private static boolean isNonInvest(Bcn bcn) {
        return !isInvest(bcn);
    }

    private static boolean isDirect(Bcn bcn) {
        return bcn.subType() == BcnSubType.DIRECT;
    }

    private static boolean isIndirect(Bcn bcn) {
        return bcn.subType() == BcnSubType.INDIRECT;
    }

    private static boolean isExternality(Bcn bcn) {
        return bcn.subType() == BcnSubType.EXTERNALITY;
    }


}
