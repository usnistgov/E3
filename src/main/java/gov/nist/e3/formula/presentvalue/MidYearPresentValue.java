package gov.nist.e3.formula.presentvalue;

public class MidYearPresentValue implements PresentValueFormula {
    @Override
    public double presentValue(double value, double rate, double timeStep) {
        if(timeStep == 0)
            return value;

        return value * Math.pow(1.0 / (1.0 + rate), timeStep - 0.5);
    }
}
