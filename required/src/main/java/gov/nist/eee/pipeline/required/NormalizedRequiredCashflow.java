package gov.nist.eee.pipeline.required;

import gov.nist.eee.util.Util;

import java.util.List;
import java.util.Objects;

public class NormalizedRequiredCashflow {
    protected final List<Double> totalCostsNonDiscounted;
    protected final List<Double> totalCostsDiscounted;
    protected final List<Double> totalBenefitsNonDiscounted;
    protected final List<Double> totalBenefitsDiscounted;
    protected final List<Double> totalCostsNonDiscountedInvest;
    protected final List<Double> totalCostsDiscountedInvest;
    protected final List<Double> totalBenefitsNonDiscountedInvest;
    protected final List<Double> totalBenefitsDiscountedInvest;
    protected final List<Double> totalCostsNonDiscountedNonInvest;
    protected final List<Double> totalCostsDiscountedNonInvest;
    protected final List<Double> totalBenefitsNonDiscountedNonInvest;
    protected final List<Double> totalBenefitsDiscountedNonInvest;
    protected final List<Double> totalCostsNonDiscountedDirect;
    protected final List<Double> totalCostsDiscountedDirect;
    protected final List<Double> totalBenefitsNonDiscountedDirect;
    protected final List<Double> totalBenefitsDiscountedDirect;
    protected final List<Double> totalCostsNonDiscountedIndirect;
    protected final List<Double> totalCostsDiscountedIndirect;
    protected final List<Double> totalBenefitsNonDiscountedIndirect;
    protected final List<Double> totalBenefitsDiscountedIndirect;
    protected final List<Double> totalCostsNonDiscountedExternal;
    protected final List<Double> totalCostsDiscountedExternal;
    protected final List<Double> totalBenefitsNonDiscountedExternal;
    protected final List<Double> totalBenefitsDiscountedExternal;

    public NormalizedRequiredCashflow(
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
        this.totalCostsNonDiscounted = totalCostsNonDiscounted;
        this.totalCostsDiscounted = totalCostsDiscounted;
        this.totalBenefitsNonDiscounted = totalBenefitsNonDiscounted;
        this.totalBenefitsDiscounted = totalBenefitsDiscounted;
        this.totalCostsNonDiscountedInvest = totalCostsNonDiscountedInvest;
        this.totalCostsDiscountedInvest = totalCostsDiscountedInvest;
        this.totalBenefitsNonDiscountedInvest = totalBenefitsNonDiscountedInvest;
        this.totalBenefitsDiscountedInvest = totalBenefitsDiscountedInvest;
        this.totalCostsNonDiscountedNonInvest = totalCostsNonDiscountedNonInvest;
        this.totalCostsDiscountedNonInvest = totalCostsDiscountedNonInvest;
        this.totalBenefitsNonDiscountedNonInvest = totalBenefitsNonDiscountedNonInvest;
        this.totalBenefitsDiscountedNonInvest = totalBenefitsDiscountedNonInvest;
        this.totalCostsNonDiscountedDirect = totalCostsNonDiscountedDirect;
        this.totalCostsDiscountedDirect = totalCostsDiscountedDirect;
        this.totalBenefitsNonDiscountedDirect = totalBenefitsNonDiscountedDirect;
        this.totalBenefitsDiscountedDirect = totalBenefitsDiscountedDirect;
        this.totalCostsNonDiscountedIndirect = totalCostsNonDiscountedIndirect;
        this.totalCostsDiscountedIndirect = totalCostsDiscountedIndirect;
        this.totalBenefitsNonDiscountedIndirect = totalBenefitsNonDiscountedIndirect;
        this.totalBenefitsDiscountedIndirect = totalBenefitsDiscountedIndirect;
        this.totalCostsNonDiscountedExternal = totalCostsNonDiscountedExternal;
        this.totalCostsDiscountedExternal = totalCostsDiscountedExternal;
        this.totalBenefitsNonDiscountedExternal = totalBenefitsNonDiscountedExternal;
        this.totalBenefitsDiscountedExternal = totalBenefitsDiscountedExternal;
    }

    public NormalizedRequiredCashflow add(NormalizedRequiredCashflow other) {
        return new NormalizedRequiredCashflow(
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

    public List<Double> totalCostsNonDiscounted() {
        return totalCostsNonDiscounted;
    }

    public List<Double> totalCostsDiscounted() {
        return totalCostsDiscounted;
    }

    public List<Double> totalBenefitsNonDiscounted() {
        return totalBenefitsNonDiscounted;
    }

    public List<Double> totalBenefitsDiscounted() {
        return totalBenefitsDiscounted;
    }

    public List<Double> totalCostsNonDiscountedInvest() {
        return totalCostsNonDiscountedInvest;
    }

    public List<Double> totalCostsDiscountedInvest() {
        return totalCostsDiscountedInvest;
    }

    public List<Double> totalBenefitsNonDiscountedInvest() {
        return totalBenefitsNonDiscountedInvest;
    }

    public List<Double> totalBenefitsDiscountedInvest() {
        return totalBenefitsDiscountedInvest;
    }

    public List<Double> totalCostsNonDiscountedNonInvest() {
        return totalCostsNonDiscountedNonInvest;
    }

    public List<Double> totalCostsDiscountedNonInvest() {
        return totalCostsDiscountedNonInvest;
    }

    public List<Double> totalBenefitsNonDiscountedNonInvest() {
        return totalBenefitsNonDiscountedNonInvest;
    }

    public List<Double> totalBenefitsDiscountedNonInvest() {
        return totalBenefitsDiscountedNonInvest;
    }

    public List<Double> totalCostsNonDiscountedDirect() {
        return totalCostsNonDiscountedDirect;
    }

    public List<Double> totalCostsDiscountedDirect() {
        return totalCostsDiscountedDirect;
    }

    public List<Double> totalBenefitsNonDiscountedDirect() {
        return totalBenefitsNonDiscountedDirect;
    }

    public List<Double> totalBenefitsDiscountedDirect() {
        return totalBenefitsDiscountedDirect;
    }

    public List<Double> totalCostsNonDiscountedIndirect() {
        return totalCostsNonDiscountedIndirect;
    }

    public List<Double> totalCostsDiscountedIndirect() {
        return totalCostsDiscountedIndirect;
    }

    public List<Double> totalBenefitsNonDiscountedIndirect() {
        return totalBenefitsNonDiscountedIndirect;
    }

    public List<Double> totalBenefitsDiscountedIndirect() {
        return totalBenefitsDiscountedIndirect;
    }

    public List<Double> totalCostsNonDiscountedExternal() {
        return totalCostsNonDiscountedExternal;
    }

    public List<Double> totalCostsDiscountedExternal() {
        return totalCostsDiscountedExternal;
    }

    public List<Double> totalBenefitsNonDiscountedExternal() {
        return totalBenefitsNonDiscountedExternal;
    }

    public List<Double> totalBenefitsDiscountedExternal() {
        return totalBenefitsDiscountedExternal;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;
        if (obj == null || obj.getClass() != this.getClass()) return false;
        var that = (NormalizedRequiredCashflow) obj;
        return Objects.equals(this.totalCostsNonDiscounted, that.totalCostsNonDiscounted) &&
                Objects.equals(this.totalCostsDiscounted, that.totalCostsDiscounted) &&
                Objects.equals(this.totalBenefitsNonDiscounted, that.totalBenefitsNonDiscounted) &&
                Objects.equals(this.totalBenefitsDiscounted, that.totalBenefitsDiscounted) &&
                Objects.equals(this.totalCostsNonDiscountedInvest, that.totalCostsNonDiscountedInvest) &&
                Objects.equals(this.totalCostsDiscountedInvest, that.totalCostsDiscountedInvest) &&
                Objects.equals(this.totalBenefitsNonDiscountedInvest, that.totalBenefitsNonDiscountedInvest) &&
                Objects.equals(this.totalBenefitsDiscountedInvest, that.totalBenefitsDiscountedInvest) &&
                Objects.equals(this.totalCostsNonDiscountedNonInvest, that.totalCostsNonDiscountedNonInvest) &&
                Objects.equals(this.totalCostsDiscountedNonInvest, that.totalCostsDiscountedNonInvest) &&
                Objects.equals(this.totalBenefitsNonDiscountedNonInvest, that.totalBenefitsNonDiscountedNonInvest) &&
                Objects.equals(this.totalBenefitsDiscountedNonInvest, that.totalBenefitsDiscountedNonInvest) &&
                Objects.equals(this.totalCostsNonDiscountedDirect, that.totalCostsNonDiscountedDirect) &&
                Objects.equals(this.totalCostsDiscountedDirect, that.totalCostsDiscountedDirect) &&
                Objects.equals(this.totalBenefitsNonDiscountedDirect, that.totalBenefitsNonDiscountedDirect) &&
                Objects.equals(this.totalBenefitsDiscountedDirect, that.totalBenefitsDiscountedDirect) &&
                Objects.equals(this.totalCostsNonDiscountedIndirect, that.totalCostsNonDiscountedIndirect) &&
                Objects.equals(this.totalCostsDiscountedIndirect, that.totalCostsDiscountedIndirect) &&
                Objects.equals(this.totalBenefitsNonDiscountedIndirect, that.totalBenefitsNonDiscountedIndirect) &&
                Objects.equals(this.totalBenefitsDiscountedIndirect, that.totalBenefitsDiscountedIndirect) &&
                Objects.equals(this.totalCostsNonDiscountedExternal, that.totalCostsNonDiscountedExternal) &&
                Objects.equals(this.totalCostsDiscountedExternal, that.totalCostsDiscountedExternal) &&
                Objects.equals(this.totalBenefitsNonDiscountedExternal, that.totalBenefitsNonDiscountedExternal) &&
                Objects.equals(this.totalBenefitsDiscountedExternal, that.totalBenefitsDiscountedExternal);
    }

    @Override
    public int hashCode() {
        return Objects.hash(totalCostsNonDiscounted, totalCostsDiscounted, totalBenefitsNonDiscounted, totalBenefitsDiscounted, totalCostsNonDiscountedInvest, totalCostsDiscountedInvest, totalBenefitsNonDiscountedInvest, totalBenefitsDiscountedInvest, totalCostsNonDiscountedNonInvest, totalCostsDiscountedNonInvest, totalBenefitsNonDiscountedNonInvest, totalBenefitsDiscountedNonInvest, totalCostsNonDiscountedDirect, totalCostsDiscountedDirect, totalBenefitsNonDiscountedDirect, totalBenefitsDiscountedDirect, totalCostsNonDiscountedIndirect, totalCostsDiscountedIndirect, totalBenefitsNonDiscountedIndirect, totalBenefitsDiscountedIndirect, totalCostsNonDiscountedExternal, totalCostsDiscountedExternal, totalBenefitsNonDiscountedExternal, totalBenefitsDiscountedExternal);
    }

    @Override
    public String toString() {
        return "NormalizedRequiredCashflow[" +
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
