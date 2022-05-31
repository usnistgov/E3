package gov.nist.e3.objects.input;

import nz.sodium.CellSink;

public record AnalysisCell(
        CellSink<Integer> cStudyPeriod,
        CellSink<Double> cInterestRate,
        CellSink<Double> cDiscountRateReal,
        CellSink<Double> cDiscountRateNominal,
        CellSink<Double> cInflationRate,
        CellSink<Double> cMarr,
        CellSink<Double> cReinvestRate,
        CellSink<Double> cFederalIncomeRate,
        CellSink<Double> cOtherIncomeRate,
        CellSink<Integer> cNumberOfAlternatives,
        CellSink<Integer> cBaseAlternative
) {
}
