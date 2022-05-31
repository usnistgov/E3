package gov.nist.e3.compute;

import gov.nist.e3.objects.input.Bcn;
import gov.nist.e3.objects.output.RequiredCashflow;
import gov.nist.e3.util.CellUtils;
import gov.nist.e3.util.tuple.Tuple5;
import nz.sodium.Cell;
import nz.sodium.Transaction;

import java.util.ArrayList;
import java.util.List;

public class RequiredCashflowPipeline {
    public final Cell<RequiredCashflow> cRequiredCashflow;

    private record IntermediateCashflow(
            List<Double> general,
            List<Double> invest,
            List<Double> nonInvest,
            List<Double> direct,
            List<Double> indirect,
            List<Double> externality
    ) {
    }

    public RequiredCashflowPipeline(
            int altId,
            List<Bcn> bcns,
            List<ResidualValuePipeline> residualValuePipelines,
            List<DiscountedPipeline> discountedPipelines,
            Cell<Integer> cStudyPeriod
    ) {
        cRequiredCashflow = define(altId, bcns, residualValuePipelines, discountedPipelines, cStudyPeriod);
    }

    private Cell<RequiredCashflow> define(
            int altId,
            List<Bcn> bcns,
            List<ResidualValuePipeline> residualValuePipelines,
            List<DiscountedPipeline> discountedPipelines,
            Cell<Integer> cStudyPeriod
    ) {
        return Transaction.run(() -> {
            var size = bcns.size();

            if (residualValuePipelines.size() != size || discountedPipelines.size() != size)
                throw new IllegalArgumentException("Cannot calculate required cashflows for mis-matched pipelines!");

            var result = new ArrayList<Cell<RequiredCashflow>>(size);

            for (int i = 0; i < size; i++) {
                var bcn = bcns.get(i);
                var valuePipeline = residualValuePipelines.get(i);
                var discountedPipeline = discountedPipelines.get(i);

                var bcnValues = new Tuple5<>(
                        bcn.isInvest(),
                        bcn.isNonInvest(),
                        bcn.isDirect(),
                        bcn.isIndirect(),
                        bcn.isExternality()
                );

                var cDiscountedIntermediateCashflow = valuePipeline.cValuesWithResidual.lift(
                        cStudyPeriod,
                        (values, studyPeriod) -> calculateIntermediateCashflow(bcnValues, values, studyPeriod)
                );
                var cNonDiscountedIntermediateCashflow = discountedPipeline.cDiscounted.lift(
                        cStudyPeriod,
                        (discounted, studyPeriod) -> calculateIntermediateCashflow(bcnValues, discounted, studyPeriod)
                );

                var cRequiredCashflows = cNonDiscountedIntermediateCashflow.lift(
                        cDiscountedIntermediateCashflow,
                        (nonDiscountedIntermediate, discountedIntermediate) ->
                                combineIntermediateCashflows(
                                        altId,
                                        bcn.isCost(),
                                        bcn.isBenefit(),
                                        nonDiscountedIntermediate,
                                        discountedIntermediate
                                )
                );

                result.add(cRequiredCashflows);
            }

            return CellUtils.mergeList(RequiredCashflow::add, result);
        });
    }

    private RequiredCashflow combineIntermediateCashflows(
            int altId,
            boolean isCost,
            boolean isBenefit,
            IntermediateCashflow discounted,
            IntermediateCashflow nonDiscounted
    ) {
        var defaultArray = new ArrayList<Double>(discounted.general.size());
        for (int i = 0; i < discounted.general.size(); i++) {
            defaultArray.add(0.0);
        }

        return new RequiredCashflow(
                altId,

                isCost ? nonDiscounted.general : defaultArray,
                isCost ? discounted.general : defaultArray,
                isBenefit ? nonDiscounted.general : defaultArray,
                isBenefit ? discounted.general : defaultArray,

                isCost ? nonDiscounted.invest : defaultArray,
                isCost ? discounted.invest : defaultArray,
                isBenefit ? nonDiscounted.invest : defaultArray,
                isBenefit ? discounted.invest : defaultArray,

                isCost ? nonDiscounted.nonInvest : defaultArray,
                isCost ? discounted.nonInvest : defaultArray,
                isBenefit ? nonDiscounted.nonInvest : defaultArray,
                isBenefit ? discounted.nonInvest : defaultArray,

                isCost ? nonDiscounted.direct : defaultArray,
                isCost ? discounted.direct : defaultArray,
                isBenefit ? nonDiscounted.direct : defaultArray,
                isBenefit ? discounted.direct : defaultArray,

                isCost ? nonDiscounted.indirect : defaultArray,
                isCost ? discounted.indirect : defaultArray,
                isBenefit ? nonDiscounted.indirect : defaultArray,
                isBenefit ? discounted.indirect : defaultArray,

                isCost ? nonDiscounted.externality : defaultArray,
                isCost ? discounted.externality : defaultArray,
                isBenefit ? nonDiscounted.externality : defaultArray,
                isBenefit ? discounted.externality : defaultArray

        );
    }

    private IntermediateCashflow calculateIntermediateCashflow(
            Tuple5<Boolean, Boolean, Boolean, Boolean, Boolean> bcnValues,
            List<Double> values,
            int studyPeriod
    ) {
        var isInvest = bcnValues.e1();
        var isNonInvest = bcnValues.e2();
        var isDirect = bcnValues.e3();
        var isIndirect = bcnValues.e4();
        var isExternality = bcnValues.e5();

        var defaultArray = new ArrayList<Double>(studyPeriod + 1);
        for (int i = 0; i < studyPeriod + 1; i++) {
            defaultArray.add(0.0);
        }

        return new IntermediateCashflow(
                values,
                isInvest ? values : defaultArray,
                isNonInvest ? values : defaultArray,
                isDirect ? values : defaultArray,
                isIndirect ? values : defaultArray,
                isExternality ? values : defaultArray
        );
    }

    public Cell<RequiredCashflow> cRequiredCashflow() {
        return cRequiredCashflow;
    }
}
