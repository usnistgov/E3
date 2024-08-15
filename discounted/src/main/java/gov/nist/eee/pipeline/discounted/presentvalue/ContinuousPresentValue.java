package gov.nist.eee.pipeline.discounted.presentvalue;

public class ContinuousPresentValue implements PresentValueFormula {
    @Override
    public double presentValue(double value, double rate, double timeStep) {
        return value * (1.0 / Math.exp(rate * timeStep));
    }
}
