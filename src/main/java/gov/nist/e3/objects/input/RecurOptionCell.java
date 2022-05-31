package gov.nist.e3.objects.input;

import nz.sodium.CellSink;

public record RecurOptionCell(
        CellSink<Integer> cInterval,
        CellSink<Integer> cEnd
) {
}
