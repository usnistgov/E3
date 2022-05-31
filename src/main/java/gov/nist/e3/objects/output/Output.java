package gov.nist.e3.objects.output;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record Output(
        List<RequiredCashflow> requiredCashflows,
        List<OptionalCashflow> optionalCashflows,
        List<MeasureSummary> measureSummaries,
        List<SensitivitySummary> sensitivitySummaries,
        List<UncertaintySummary> uncertaintySummaries
) {
}
