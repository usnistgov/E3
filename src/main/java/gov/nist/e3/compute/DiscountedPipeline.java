package gov.nist.e3.compute;

import gov.nist.e3.formula.presentvalue.ContinuousPresentValue;
import gov.nist.e3.formula.presentvalue.EndOfYearPresentValue;
import gov.nist.e3.formula.presentvalue.MidYearPresentValue;
import gov.nist.e3.formula.presentvalue.PresentValueFormula;
import gov.nist.e3.objects.input.TimestepComp;
import nz.sodium.Cell;
import nz.sodium.Transaction;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class DiscountedPipeline {
    public final Cell<List<Double>> cDiscounted;

    public DiscountedPipeline(
            Cell<List<Double>> cValues,
            Cell<Double> cDiscountRate,
            TimestepComp timestepComp
    ) {
        cDiscounted = define(cValues, cDiscountRate, timestepComp);
    }

    private Cell<List<Double>> define(
            Cell<List<Double>> cValues,
            Cell<Double> cDiscountRate,
            TimestepComp timestepComp
    ) {
        return Transaction.run(() -> {
            var presentValueFormula = getPresentValueFormula(timestepComp);
            return cValues.lift(cDiscountRate, (values, rate) -> discountValues(values, rate, presentValueFormula));
        });
    }

    private PresentValueFormula getPresentValueFormula(@Nullable TimestepComp timestepComp) {
        if(timestepComp == null)
            return new EndOfYearPresentValue();

        return switch(timestepComp) {
            case END_OF_YEAR -> new EndOfYearPresentValue();
            case MID_YEAR -> new MidYearPresentValue();
            case CONTINUOUS -> new ContinuousPresentValue();
        };
    }

    private List<Double> discountValues(List<Double> values, double rate, PresentValueFormula formula) {
        var result = new ArrayList<Double>(values.size());

        for (int i = 0; i < values.size(); i++) {
            result.add(formula.presentValue(values.get(i), rate, i));
        }

        return result;
    }

}
