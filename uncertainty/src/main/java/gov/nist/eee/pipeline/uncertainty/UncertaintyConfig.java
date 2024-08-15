package gov.nist.eee.pipeline.uncertainty;

public record UncertaintyConfig(int maxIterations, int minIterations, int stride, double tolerance) {
}
