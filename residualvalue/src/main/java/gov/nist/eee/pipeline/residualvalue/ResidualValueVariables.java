package gov.nist.eee.pipeline.residualvalue;

public record ResidualValueVariables(
        int initial,
        boolean isRecurNull,
        boolean hasResidualValue,
        boolean hasResidualValueOnly
) {
}
