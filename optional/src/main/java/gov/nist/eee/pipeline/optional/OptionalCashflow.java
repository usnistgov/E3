package gov.nist.eee.pipeline.optional;

import gov.nist.eee.util.Util;

import java.util.ArrayList;
import java.util.List;
import java.util.function.BiFunction;

public record OptionalCashflow(
        int altId,
        String tag,
        List<Double> totalTagCashflowDiscounted,
        List<Double> totalTagCashflowNonDiscounted,
        List<Double> totalTagQuantity,
        String units
) {
    public OptionalCashflow add(OptionalCashflow other){
        if(other.altId != this.altId)
            throw new IllegalArgumentException("Cannot add optional cashflows together from different alternatives.");

        if(!other.units.equals(this.units))
            throw new IllegalStateException("Cannot add optional cashflows together with different units.");

        return new OptionalCashflow(
                this.altId,
                this.tag,
                Util.elementwiseAdd(this.totalTagCashflowDiscounted, other.totalTagCashflowDiscounted),
                Util.elementwiseAdd(this.totalTagCashflowNonDiscounted, other.totalTagCashflowNonDiscounted),
                Util.elementwiseAdd(this.totalTagQuantity, other.totalTagQuantity),
                this.units
        );
    }
}