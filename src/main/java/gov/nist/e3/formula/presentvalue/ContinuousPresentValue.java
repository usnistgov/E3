package gov.nist.e3.formula.presentvalue;

public class ContinuousPresentValue implements PresentValueFormula {
    @Override
    public double presentValue(double value, double rate, double timeStep) {
        return value * (1.0 / Math.exp(rate * timeStep));
    }
}
