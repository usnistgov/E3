package gov.nist.eee.pipeline.required;

import java.util.List;

public record IntermediateCashflow(
        List<Double> general,
        List<Double> invest,
        List<Double> nonInvest,
        List<Double> direct,
        List<Double> indirect,
        List<Double> externality
) {
}