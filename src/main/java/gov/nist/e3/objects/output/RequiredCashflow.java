package gov.nist.e3.objects.output;

import gov.nist.e3.util.Util;

import java.util.List;

public record RequiredCashflow(
        int altId,

        List<Double> totalCostsNonDiscounted,
        List<Double> totalCostsDiscounted,
        List<Double> totalBenefitsNonDiscounted,
        List<Double> totalBenefitsDiscounted,

        List<Double> totalCostsNonDiscountedInvest,
        List<Double> totalCostsDiscountedInvest,
        List<Double> totalBenefitsNonDiscountedInvest,
        List<Double> totalBenefitsDiscountedInvest,

        List<Double> totalCostsNonDiscountedNonInvest,
        List<Double> totalCostsDiscountedNonInvest,
        List<Double> totalBenefitsNonDiscountedNonInvest,
        List<Double> totalBenefitsDiscountedNonInvest,

        List<Double> totalCostsNonDiscountedDirect,
        List<Double> totalCostsDiscountedDirect,
        List<Double> totalBenefitsNonDiscountedDirect,
        List<Double> totalBenefitsDiscountedDirect,

        List<Double> totalCostsNonDiscountedIndirect,
        List<Double> totalCostsDiscountedIndirect,
        List<Double> totalBenefitsNonDiscountedIndirect,
        List<Double> totalBenefitsDiscountedIndirect,

        List<Double> totalCostsNonDiscountedExternal,
        List<Double> totalCostsDiscountedExternal,
        List<Double> totalBenefitsNonDiscountedExternal,
        List<Double> totalBenefitsDiscountedExternal
) {
    public RequiredCashflow add(RequiredCashflow other) {
        if(this.altId != other.altId)
            throw new IllegalArgumentException("Cannot add required cashflows together from different alts");

        return new RequiredCashflow(
                this.altId,

                Util.elementwiseAdd(this.totalCostsNonDiscounted, other.totalCostsNonDiscounted),
                Util.elementwiseAdd(this.totalCostsDiscounted, other.totalCostsDiscounted),
                Util.elementwiseAdd(this.totalBenefitsNonDiscounted, other.totalBenefitsNonDiscounted),
                Util.elementwiseAdd(this.totalBenefitsDiscounted, other.totalBenefitsDiscounted),

                Util.elementwiseAdd(this.totalCostsNonDiscountedInvest, other.totalCostsNonDiscountedInvest),
                Util.elementwiseAdd(this.totalCostsDiscountedInvest, other.totalCostsDiscountedInvest),
                Util.elementwiseAdd(this.totalBenefitsNonDiscountedInvest, other.totalBenefitsNonDiscountedInvest),
                Util.elementwiseAdd(this.totalBenefitsDiscountedInvest, other.totalBenefitsDiscountedInvest),

                Util.elementwiseAdd(this.totalCostsNonDiscountedNonInvest, other.totalCostsNonDiscountedNonInvest),
                Util.elementwiseAdd(this.totalCostsDiscountedNonInvest, other.totalCostsDiscountedNonInvest),
                Util.elementwiseAdd(this.totalBenefitsNonDiscountedNonInvest, other.totalBenefitsNonDiscountedNonInvest),
                Util.elementwiseAdd(this.totalBenefitsDiscountedNonInvest, other.totalBenefitsDiscountedNonInvest),

                Util.elementwiseAdd(this.totalCostsNonDiscountedDirect, other.totalCostsNonDiscountedDirect),
                Util.elementwiseAdd(this.totalCostsDiscountedDirect, other.totalCostsDiscountedDirect),
                Util.elementwiseAdd(this.totalBenefitsNonDiscountedDirect, other.totalBenefitsNonDiscountedDirect),
                Util.elementwiseAdd(this.totalBenefitsDiscountedDirect, other.totalBenefitsDiscountedDirect),

                Util.elementwiseAdd(this.totalCostsNonDiscountedIndirect, other.totalCostsNonDiscountedIndirect),
                Util.elementwiseAdd(this.totalCostsDiscountedIndirect, other.totalCostsDiscountedIndirect),
                Util.elementwiseAdd(this.totalBenefitsNonDiscountedIndirect, other.totalBenefitsNonDiscountedIndirect),
                Util.elementwiseAdd(this.totalBenefitsDiscountedIndirect, other.totalBenefitsDiscountedIndirect),

                Util.elementwiseAdd(this.totalCostsNonDiscountedExternal, other.totalCostsNonDiscountedExternal),
                Util.elementwiseAdd(this.totalCostsDiscountedExternal, other.totalCostsDiscountedExternal),
                Util.elementwiseAdd(this.totalBenefitsNonDiscountedExternal, other.totalBenefitsNonDiscountedExternal),
                Util.elementwiseAdd(this.totalBenefitsDiscountedExternal, other.totalBenefitsDiscountedExternal)
        );
    }
}
