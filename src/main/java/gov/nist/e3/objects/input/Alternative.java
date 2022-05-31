package gov.nist.e3.objects.input;

import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public record Alternative(
        int id,
        @Nullable
        String name,
        @NotNull
        List<Integer> bcns
) {
}
