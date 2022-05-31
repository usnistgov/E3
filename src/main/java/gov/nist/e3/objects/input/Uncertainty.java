package gov.nist.e3.objects.input;

import org.jetbrains.annotations.NotNull;

import java.util.List;

public record Uncertainty(
        int id,
        @NotNull List<UncertaintyVariable> variables,
        Integer seed
) {
}
