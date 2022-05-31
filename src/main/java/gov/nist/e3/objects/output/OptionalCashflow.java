package gov.nist.e3.objects.output;

import gov.nist.e3.util.Util;

import java.util.List;

public record OptionalCashflow(
        int altId,
        String tag,
        List<Double> totalTagCashflowDiscounted,
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
                Util.elementwiseAdd(this.totalTagQuantity, other.totalTagQuantity),
                this.units
        );
    }
}
