package gov.nist.e3.formula.presentvalue;

@FunctionalInterface
public interface PresentValueFormula {
    double presentValue(double value, double rate, double timeStep);
}
