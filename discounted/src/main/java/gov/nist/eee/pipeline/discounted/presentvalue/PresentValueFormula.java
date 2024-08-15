package gov.nist.eee.pipeline.discounted.presentvalue;

/**
 * Functional interface that represents a present value formula.
 */
@FunctionalInterface
public interface PresentValueFormula {
    /**
     * Calculate the present value of the given value with the given rate and time-step.
     *
     * @param value the value to get the present value of.
     * @param rate the discount rate to calculate with.
     * @param timeStep the time-step to calculate for.
     * @return the present value of the given value.
     */
    double presentValue(double value, double rate, double timeStep);
}
