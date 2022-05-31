package gov.nist.e3.objects.input;

import nz.sodium.CellSink;

public record BcnCell(
        CellSink<Integer> cInitialOccurrence,
        CellSink<Integer> cLife,
        CellSink<Double> cQuantityValue,
        CellSink<Double> cQuantity
) {
}
