package gov.nist.e3.formula.presentvalue;

public class EndOfYearPresentValue implements PresentValueFormula{
    @Override
    public double presentValue(double value, double rate, double timeStep) {
        if(value == 0.0)
            return 0.0;

        if(timeStep == 0.0)
            return value;

        return value * Math.pow(1.0 / (1.0 + rate), timeStep);
    }
}
