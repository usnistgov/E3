package gov.nist.eee.pipeline.sensitivity;

import gov.nist.eee.pipeline.measures.MeasureSummary;

import java.util.List;
import java.util.Map;

public record SensitivitySummary(int id, Map<Integer, List<MeasureSummary>> alternativeSummaries) {
}
