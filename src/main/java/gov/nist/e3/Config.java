package gov.nist.e3;

import gov.nist.e3.objects.input.OutputType;

import static gov.nist.e3.objects.input.OutputType.*;

import gov.nist.e3.util.dependency.DependencyGraph;

import java.util.List;

public class Config {
    private Config() {
        throw new UnsupportedOperationException("Cannot instantiate static utility class");
    }

    public static final int MAX_DIGITS = 60;
    public static final int MAX_DECIMAL_PLACES = 30;

    public static final String TREE_PATTERN = "[.\\[\\]]+";

    public static final DependencyGraph<OutputType> E3_DEPENDENCY_GRAPH = new DependencyGraph<>();

    public static final double UNCERTAINTY_MAX_ITERATIONS = 50_000;
    public static final double UNCERTAINTY_TOLERANCE = 0.001;   // 0.1%
    public static final double IRR_TOLERANCE = 0.0001;          // 0.01%

    static {
        E3_DEPENDENCY_GRAPH.add(REQUIRED);
        E3_DEPENDENCY_GRAPH.add(OPTIONAL);
        E3_DEPENDENCY_GRAPH.add(MEASURES, List.of(REQUIRED, OPTIONAL));
        E3_DEPENDENCY_GRAPH.add(SENSITIVITY, List.of(MEASURES));
        E3_DEPENDENCY_GRAPH.add(UNCERTAINTY, List.of(MEASURES));
    }
}
