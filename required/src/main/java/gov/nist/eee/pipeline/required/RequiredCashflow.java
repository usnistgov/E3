package gov.nist.eee.pipeline.required;


import java.util.Objects;

public class RequiredCashflow extends NormalizedRequiredCashflow {
    private final int altId;

    public RequiredCashflow(int altId, NormalizedRequiredCashflow normalizedCashflow) {
        super(
                normalizedCashflow.totalCostsNonDiscounted,
                normalizedCashflow.totalCostsDiscounted,
                normalizedCashflow.totalBenefitsNonDiscounted,
                normalizedCashflow.totalBenefitsDiscounted,
                normalizedCashflow.totalCostsNonDiscountedInvest,
                normalizedCashflow.totalCostsDiscountedInvest,
                normalizedCashflow.totalBenefitsNonDiscountedInvest,
                normalizedCashflow.totalBenefitsDiscountedInvest,
                normalizedCashflow.totalCostsNonDiscountedNonInvest,
                normalizedCashflow.totalCostsDiscountedNonInvest,
                normalizedCashflow.totalBenefitsNonDiscountedNonInvest,
                normalizedCashflow.totalBenefitsDiscountedNonInvest,
                normalizedCashflow.totalCostsNonDiscountedDirect,
                normalizedCashflow.totalCostsDiscountedDirect,
                normalizedCashflow.totalBenefitsNonDiscountedDirect,
                normalizedCashflow.totalBenefitsDiscountedDirect,
                normalizedCashflow.totalCostsNonDiscountedIndirect,
                normalizedCashflow.totalCostsDiscountedIndirect,
                normalizedCashflow.totalBenefitsNonDiscountedIndirect,
                normalizedCashflow.totalBenefitsDiscountedIndirect,
                normalizedCashflow.totalCostsNonDiscountedExternal,
                normalizedCashflow.totalCostsDiscountedExternal,
                normalizedCashflow.totalBenefitsNonDiscountedExternal,
                normalizedCashflow.totalBenefitsDiscountedExternal
        );

        this.altId = altId;
    }

    public int altId() {
        return altId;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;
        if (obj == null || obj.getClass() != this.getClass()) return false;
        var that = (RequiredCashflow) obj;
        return this.altId == that.altId && super.equals(obj);
    }

    @Override
    public int hashCode() {
        return Objects.hash(altId, super.hashCode());
    }

    @Override
    public String toString() {
        return "RequiredCashflow[" +
                "altId=" + altId + ", " +
                "totalCostsNonDiscounted=" + totalCostsNonDiscounted + ", " +
                "totalCostsDiscounted=" + totalCostsDiscounted + ", " +
                "totalBenefitsNonDiscounted=" + totalBenefitsNonDiscounted + ", " +
                "totalBenefitsDiscounted=" + totalBenefitsDiscounted + ", " +
                "totalCostsNonDiscountedInvest=" + totalCostsNonDiscountedInvest + ", " +
                "totalCostsDiscountedInvest=" + totalCostsDiscountedInvest + ", " +
                "totalBenefitsNonDiscountedInvest=" + totalBenefitsNonDiscountedInvest + ", " +
                "totalBenefitsDiscountedInvest=" + totalBenefitsDiscountedInvest + ", " +
                "totalCostsNonDiscountedNonInvest=" + totalCostsNonDiscountedNonInvest + ", " +
                "totalCostsDiscountedNonInvest=" + totalCostsDiscountedNonInvest + ", " +
                "totalBenefitsNonDiscountedNonInvest=" + totalBenefitsNonDiscountedNonInvest + ", " +
                "totalBenefitsDiscountedNonInvest=" + totalBenefitsDiscountedNonInvest + ", " +
                "totalCostsNonDiscountedDirect=" + totalCostsNonDiscountedDirect + ", " +
                "totalCostsDiscountedDirect=" + totalCostsDiscountedDirect + ", " +
                "totalBenefitsNonDiscountedDirect=" + totalBenefitsNonDiscountedDirect + ", " +
                "totalBenefitsDiscountedDirect=" + totalBenefitsDiscountedDirect + ", " +
                "totalCostsNonDiscountedIndirect=" + totalCostsNonDiscountedIndirect + ", " +
                "totalCostsDiscountedIndirect=" + totalCostsDiscountedIndirect + ", " +
                "totalBenefitsNonDiscountedIndirect=" + totalBenefitsNonDiscountedIndirect + ", " +
                "totalBenefitsDiscountedIndirect=" + totalBenefitsDiscountedIndirect + ", " +
                "totalCostsNonDiscountedExternal=" + totalCostsNonDiscountedExternal + ", " +
                "totalCostsDiscountedExternal=" + totalCostsDiscountedExternal + ", " +
                "totalBenefitsNonDiscountedExternal=" + totalBenefitsNonDiscountedExternal + ", " +
                "totalBenefitsDiscountedExternal=" + totalBenefitsDiscountedExternal + ']';
    }

}
