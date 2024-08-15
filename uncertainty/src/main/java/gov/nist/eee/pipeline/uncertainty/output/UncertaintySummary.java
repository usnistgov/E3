package gov.nist.eee.pipeline.uncertainty.output;

import java.util.Map;

public record UncertaintySummary(int id, Map<Integer, UncertaintyMeasureSummary> alternatives) {
}
