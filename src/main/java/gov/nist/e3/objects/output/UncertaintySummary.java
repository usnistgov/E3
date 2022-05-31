package gov.nist.e3.objects.output;

import java.util.Map;

public record UncertaintySummary(
        int id,
        Map<Integer, UncertaintyMeasureSummary> alternatives
) {
}
