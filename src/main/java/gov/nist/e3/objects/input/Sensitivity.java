package gov.nist.e3.objects.input;

import java.util.List;

public record Sensitivity(
        int id,
        List<Integer> altIds,
        String variable,
        SensitivityDiffType diffType,
        double diffValue
) {
}
