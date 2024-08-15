package gov.nist.eee.pipeline.sensitivity.input;

import gov.nist.eee.object.InputExtension;

import java.util.List;

@InputExtension(key = "sensitivityObjects", schema = "/sensitivity-schema.json", container = List.class)
public record Sensitivity(
        int id,
        List<Integer> altIds,
        String variable,
        SensitivityDiffType diffType,
        double diffValue
) {
}
