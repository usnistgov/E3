package gov.nist.eee.pipeline.edges;

public class Formula {
    public static double annulaizedROI(double netBenefit, double investCost, double horizon) {
        if(investCost == 0 || horizon == 0)
            throw new RuntimeException("Cannot divide by zero!");

        return ((netBenefit - investCost) * 100.0) / horizon;
    }
}
