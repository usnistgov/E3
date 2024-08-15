package gov.nist.eee.object.input;

import org.jetbrains.annotations.Nullable;

import java.util.List;

/**
 * Record representing the analysis object for an E3 request.
 *
 * @param type The {@link AnalysisType}. Currently only used for reporting.
 * @param projectType The {@link ProjectType}. Currently only used for reporting.
 * @param outputObjects A list of name that denotes which pipeline outputs to output in the response.
 * @param studyPeriod The number of time steps in this analysis.
 * @param timestepValue
 * @param timestepComp
 * @param outputReal
 * @param interestRate
 * @param discountRateReal
 * @param discountRateNominal
 * @param inflationRate
 * @param marr
 * @param reinvestRate
 * @param federalIncomeRate
 * @param otherIncomeRate
 * @param location The {@link Location} of the request.
 * @param baseAlternative The ID of the baseline alternative in this request.
 */
public record Analysis (
    @Nullable AnalysisType type,
    @Nullable ProjectType projectType,
    @Nullable List<String> outputObjects,
    @Nullable Integer studyPeriod,
    @Nullable TimestepValue timestepValue,
    @Nullable TimestepComp timestepComp,
    @Nullable Boolean outputReal,
    @Nullable Double interestRate,
    @Nullable Double discountRateReal,
    @Nullable Double discountRateNominal,
    @Nullable Double inflationRate,
    @Nullable Double marr,
    @Nullable Double reinvestRate,
    @Nullable Double federalIncomeRate,
    @Nullable Double otherIncomeRate,
    @Nullable Location location,
    int baseAlternative
){}