package gov.nist.eee.pipeline.uncertainty.input;


import gov.nist.eee.object.InputExtension;

import java.util.List;

@InputExtension(key = "uncertainty", schema = "/uncertainty-schema.json", container = List.class)
public record Uncertainty(int id, List<UncertaintyVariable> variables, Integer seed) {
}
