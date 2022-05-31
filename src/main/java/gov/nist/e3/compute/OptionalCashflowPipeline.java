package gov.nist.e3.compute;

import gov.nist.e3.objects.input.Bcn;
import gov.nist.e3.objects.output.OptionalCashflow;
import gov.nist.e3.util.CellUtils;
import nz.sodium.Cell;
import nz.sodium.Transaction;

import java.util.ArrayList;
import java.util.List;

public class OptionalCashflowPipeline {
    public final Cell<OptionalCashflow> cOptionalCashflows;

    public OptionalCashflowPipeline(
            int altId,
            String tag,
            List<Bcn> bcns,
            List<QuantityPipeline> quantityPipelines,
            List<DiscountedPipeline> discountedPipelines
    ) {
        cOptionalCashflows = define(altId, tag, bcns, quantityPipelines, discountedPipelines);
    }

    public Cell<OptionalCashflow> define(
            int altId,
            String tag,
            List<Bcn> bcns,
            List<QuantityPipeline> quantityPipelines,
            List<DiscountedPipeline> discountedPipelines
    ) {
        return Transaction.run(() -> {
            var optionals = createCashflows(altId, tag, bcns, quantityPipelines, discountedPipelines);
            return CellUtils.mergeList(OptionalCashflow::add, optionals);
        });
    }

    public static List<Cell<OptionalCashflow>> createCashflows(
            int altId, 
            String tag, 
            List<Bcn> bcns, 
            List<QuantityPipeline> quantityPipelines, 
            List<DiscountedPipeline> discountedPipelines
    ) {
        var num = bcns.size();

        if (quantityPipelines.size() != num || discountedPipelines.size() != num)
            throw new IllegalArgumentException("BCNs must have a corresponding quantity and discount pipeline.");

        var result = new ArrayList<Cell<OptionalCashflow>>(num);

        for (int i = 0; i < num; i++) {
            var unit = bcns.get(i).quantityUnit();
            var cQuantities = quantityPipelines.get(i).cQuantities;
            var cDiscounts = discountedPipelines.get(i).cDiscounted;

            var cOptional = cQuantities.lift(
                    cDiscounts,
                    (quantities, discounts) -> new OptionalCashflow(altId, tag, quantities, discounts, unit)
            );

            result.add(cOptional);
        }

        return result;
    }
}
