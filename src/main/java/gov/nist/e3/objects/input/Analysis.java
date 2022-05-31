package gov.nist.e3.objects.input;

import gov.nist.e3.tree.ToTree;
import gov.nist.e3.tree.Tree;
import gov.nist.e3.util.ToCell;
import nz.sodium.CellSink;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;
import java.util.Objects;

public final class Analysis implements ToTree<String, CellSink<? extends Number>>, ToCell<AnalysisCell> {
    private final @Nullable AnalysisType type;
    private final @Nullable ProjectType projectType;
    private final @Nullable List<OutputType> outputObjects;
    private final @Nullable Integer studyPeriod;
    private final @Nullable TimestepValue timestepValue;
    private final @Nullable TimestepComp timestepComp;
    private final @Nullable Boolean outputReal;
    private final @Nullable Double interestRate;
    private final @Nullable Double discountRateReal;
    private final @Nullable Double discountRateNominal;
    private final @Nullable Double inflationRate;
    private final @Nullable Double marr;
    private final @Nullable Double reinvestRate;
    private final @Nullable Double federalIncomeRate;
    private final @Nullable Double otherIncomeRate;
    private final @Nullable Location location;
    private final int numberOfAlternatives;
    private final int baseAlternative;

    private AnalysisCell cell;

    public Analysis(
            @Nullable AnalysisType type,
            @Nullable ProjectType projectType,
            @Nullable List<OutputType> outputObjects,
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
            int numberOfAlternatives,
            int baseAlternative
    ) {
        if (outputObjects == null)
            outputObjects = List.of(OutputType.REQUIRED);
        this.type = type;
        this.projectType = projectType;
        this.outputObjects = outputObjects;
        this.studyPeriod = studyPeriod;
        this.timestepValue = timestepValue;
        this.timestepComp = timestepComp;
        this.outputReal = outputReal;
        this.interestRate = interestRate;
        this.discountRateReal = discountRateReal;
        this.discountRateNominal = discountRateNominal;
        this.inflationRate = inflationRate;
        this.marr = marr;
        this.reinvestRate = reinvestRate;
        this.federalIncomeRate = federalIncomeRate;
        this.otherIncomeRate = otherIncomeRate;
        this.location = location;
        this.numberOfAlternatives = numberOfAlternatives;
        this.baseAlternative = baseAlternative;
    }

    @Override
    public Tree<String, CellSink<? extends Number>> toTree() {
        var result = Tree.<String, CellSink<? extends Number>>create();

        result.add("studyPeriod", this.cell.cStudyPeriod());
        result.add("interestRate", this.cell.cInterestRate());
        result.add("discountRateReal", this.cell.cDiscountRateReal());
        result.add("discountRateNominal", this.cell.cDiscountRateNominal());
        result.add("inflationRate", this.cell.cInflationRate());
        result.add("marr", this.cell.cMarr());
        result.add("reinvestRate", this.cell.cReinvestRate());
        result.add("federalIncomeRate", this.cell.cFederalIncomeRate());
        result.add("otherIncomeRate", this.cell.cOtherIncomeRate());
        result.add("numberOfAlternatives", this.cell.cNumberOfAlternatives());
        result.add("baseAlternative", this.cell.cBaseAlternative());

        return result;
    }

    @Override
    public AnalysisCell toCell() {
        if (this.cell == null) {
            this.cell = new AnalysisCell(
                    new CellSink<>(studyPeriod),
                    new CellSink<>(interestRate),
                    new CellSink<>(discountRateReal),
                    new CellSink<>(discountRateNominal),
                    new CellSink<>(inflationRate),
                    new CellSink<>(marr),
                    new CellSink<>(reinvestRate),
                    new CellSink<>(federalIncomeRate),
                    new CellSink<>(otherIncomeRate),
                    new CellSink<>(numberOfAlternatives),
                    new CellSink<>(baseAlternative)
            );
        }

        return cell;
    }

    public @Nullable AnalysisType type() {
        return type;
    }

    public @Nullable ProjectType projectType() {
        return projectType;
    }

    public @Nullable List<OutputType> outputObjects() {
        return outputObjects;
    }

    public @NotNull Integer studyPeriod() {
        return studyPeriod;
    }

    public @Nullable TimestepValue timestepValue() {
        return timestepValue;
    }

    public @Nullable TimestepComp timestepComp() {
        return timestepComp;
    }

    public @Nullable Boolean outputReal() {
        return outputReal;
    }

    public @Nullable Double interestRate() {
        return interestRate;
    }

    public @Nullable Double discountRateReal() {
        return discountRateReal;
    }

    public @Nullable Double discountRateNominal() {
        return discountRateNominal;
    }

    public @Nullable Double inflationRate() {
        return inflationRate;
    }

    public @Nullable Double marr() {
        return marr;
    }

    public @Nullable Double reinvestRate() {
        return reinvestRate;
    }

    public @Nullable Double federalIncomeRate() {
        return federalIncomeRate;
    }

    public @Nullable Double otherIncomeRate() {
        return otherIncomeRate;
    }

    public @Nullable Location location() {
        return location;
    }

    public int numberOfAlternatives() {
        return numberOfAlternatives;
    }

    public int baseAlternative() {
        return baseAlternative;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;
        if (obj == null || obj.getClass() != this.getClass()) return false;
        var that = (Analysis) obj;
        return Objects.equals(this.type, that.type) &&
                Objects.equals(this.projectType, that.projectType) &&
                Objects.equals(this.outputObjects, that.outputObjects) &&
                Objects.equals(this.studyPeriod, that.studyPeriod) &&
                Objects.equals(this.timestepValue, that.timestepValue) &&
                Objects.equals(this.timestepComp, that.timestepComp) &&
                Objects.equals(this.outputReal, that.outputReal) &&
                Objects.equals(this.interestRate, that.interestRate) &&
                Objects.equals(this.discountRateReal, that.discountRateReal) &&
                Objects.equals(this.discountRateNominal, that.discountRateNominal) &&
                Objects.equals(this.inflationRate, that.inflationRate) &&
                Objects.equals(this.marr, that.marr) &&
                Objects.equals(this.reinvestRate, that.reinvestRate) &&
                Objects.equals(this.federalIncomeRate, that.federalIncomeRate) &&
                Objects.equals(this.otherIncomeRate, that.otherIncomeRate) &&
                Objects.equals(this.location, that.location) &&
                this.numberOfAlternatives == that.numberOfAlternatives &&
                this.baseAlternative == that.baseAlternative;
    }

    @Override
    public int hashCode() {
        return Objects.hash(type, projectType, outputObjects, studyPeriod, timestepValue, timestepComp, outputReal, interestRate, discountRateReal, discountRateNominal, inflationRate, marr, reinvestRate, federalIncomeRate, otherIncomeRate, location, numberOfAlternatives, baseAlternative);
    }

    @Override
    public String toString() {
        return "Analysis[" +
                "type=" + type + ", " +
                "projectType=" + projectType + ", " +
                "outputObjects=" + outputObjects + ", " +
                "studyPeriod=" + studyPeriod + ", " +
                "timestepValue=" + timestepValue + ", " +
                "timestepComp=" + timestepComp + ", " +
                "outputReal=" + outputReal + ", " +
                "interestRate=" + interestRate + ", " +
                "discountRateReal=" + discountRateReal + ", " +
                "discountRateNominal=" + discountRateNominal + ", " +
                "inflationRate=" + inflationRate + ", " +
                "marr=" + marr + ", " +
                "reinvestRate=" + reinvestRate + ", " +
                "federalIncomeRate=" + federalIncomeRate + ", " +
                "otherIncomeRate=" + otherIncomeRate + ", " +
                "location=" + location + ", " +
                "numberOfAlternatives=" + numberOfAlternatives + ", " +
                "baseAlternative=" + baseAlternative + ']';
    }
}