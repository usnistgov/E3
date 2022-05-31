package gov.nist.e3.formula;

import gov.nist.e3.Config;
import gov.nist.e3.util.Util;
import org.apache.commons.math3.analysis.solvers.RiddersSolver;
import org.apache.commons.math3.util.FastMath;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class Formula {
    private static final Logger log = LoggerFactory.getLogger(Formula.class);

    private Formula() {
        throw new IllegalStateException("Cannot instantiate static utility class");
    }

    /**
     * Compounds the given list of values.
     *
     * @param values The values to compound.
     * @return The compounded values.
     */
    public static List<Double> compound(List<Double> values) {
        return Util.scan(values, 1.0, Formula::compound);
    }

    /**
     * The formula for compounding values. Takes a previous and current value and returns the result of the calculation.
     *
     * @param previous The previous value to compound with.
     * @param current  The current modifier to compound by.
     * @return The result of the compounding calculation.
     */
    public static double compound(double previous, double current) {
        return previous * (current + 1.0);
    }

    /**
     * Discounts the given value to its present value.
     *
     * @param value    The value to discount.
     * @param rate     The rate of discounting.
     * @param timeStep The amount of time in the future to discount.
     * @return The value discounted to its present value.
     */
    public static double presentValue(double value, double rate, double timeStep) {
        if (value == 0.0)
            return 0.0;

        if (timeStep == 0.0)
            return value;

        return value * Math.pow(1.0 / (1.0 + rate), timeStep);
    }

    public static double continuousPresentValue(double value, double rate, double timeStep) {
        return value * (1.0 / Math.exp(rate * timeStep));
    }

    public static double midYearPresentValue(double value, double rate, double timeStep) {
        if (timeStep == 0)
            return value;

        return Math.pow(value * (1.0 / (1.0 + rate)), timeStep - 0.5);
    }

    public static double irr(List<Double> values) {
        return irr(values, Config.IRR_TOLERANCE);
    }

    public static double irr(List<Double> values, double tolerance) {
        var ridders = new RiddersSolver(tolerance);

        return ridders.solve(100, (double r) -> sumIrr(values, r), -0.0, 1.0);
    }

    public static double sumIrr(List<Double> values, double r) {
        var sum = 0.0;
        for (int i = 0; i < values.size(); i++) {
            sum += values.get(i) / FastMath.pow(1 + r, i);
        }
        return sum;
    }
}