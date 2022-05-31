package gov.nist.e3.objects.input;

import gov.nist.e3.tree.ToTree;
import gov.nist.e3.tree.Tree;
import gov.nist.e3.web.validation.ComplexValidationTest;
import gov.nist.e3.web.validation.result.ValidationResult;
import nz.sodium.CellSink;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;
import java.util.Objects;
import java.util.stream.Stream;

public record Input(
        @NotNull
        Analysis analysisObject,
        @NotNull
        List<Alternative> alternativeObjects,
        @NotNull
        List<Bcn> bcnObjects,
        @Nullable
        List<Sensitivity> sensitivityObjects,
        @Nullable
        List<Uncertainty> uncertainty
) implements ToTree<String, CellSink<? extends Number>> {
    @Override
    public Tree<String, CellSink<? extends Number>> toTree() {
        var result = Tree.<String, CellSink<? extends Number>>create();

        result.addTree("analysisObject", analysisObject().toTree());

        var bcnTrees = Tree.<String, CellSink<? extends Number>>create();
        for (int i = 0; i < bcnObjects().size(); i++) {
            bcnTrees.addTree(Integer.toString(i), bcnObjects().get(i).toTree());
        }
        result.addTree("bcnObjects", bcnTrees);

        return result;
    }

    @ComplexValidationTest
    public ValidationResult analysisNumAlternativesEqualsActualNumAlternatives() {
        var numAnalysisAlternatives = analysisObject().numberOfAlternatives();
        var numActualAlternatives = alternativeObjects().size();

        if (numAnalysisAlternatives == numActualAlternatives)
            return new ValidationResult.Success();

        return new ValidationResult.Failure(String.format(
                "Analysis class declares %d alternatives but actually has %d.",
                numAnalysisAlternatives,
                numActualAlternatives
        ));
    }

    @ComplexValidationTest
    public ValidationResult baselineAlternativeExists() {
        var baselineAltId = analysisObject().baseAlternative();
        if (alternativeObjects().stream().anyMatch(alt -> alt.id() == baselineAltId))
            return new ValidationResult.Success();

        return new ValidationResult.Failure(
                String.format("Could not find baseline alternative with ID %d.", baselineAltId)
        );
    }

    @ComplexValidationTest
    public ValidationResult atLeastTwoRatesDefined() {
        var discountRateReal = analysisObject().discountRateReal();
        var discountRateNominal = analysisObject().discountRateNominal();
        var inflationRate = analysisObject().inflationRate();

        var numDefined = Stream.of(discountRateReal, discountRateNominal, inflationRate)
                .filter(Objects::nonNull)
                .count();

        if (numDefined >= 2)
            return new ValidationResult.Success();

        return new ValidationResult.Failure(
                "At least two rates must be defined. Given\nDiscount Rate Real " + discountRateReal +
                        "\nDiscount Rate Nominal " + discountRateNominal + "\nInterest Rate " + inflationRate
        );
    }

    @ComplexValidationTest
    public ValidationResult bcnRecurVarValueEqualToStudyPeriod() {
        int actualStudyPeriod = analysisObject().studyPeriod() + 1;

        for (var bcn : bcnObjects()) {
            if (bcn.recur() == null)
                continue;

            var varValue = bcn.recur().varValue();

            if (varValue != null && varValue.size() != 1 && varValue.size() != actualStudyPeriod) {
                return new ValidationResult.Failure(
                        "Recur VarValue for BCN " + bcn.id() + " must be either null, a single value, or an array of " +
                                "values equal to the study period " + actualStudyPeriod + "."
                );
            }
        }

        return new ValidationResult.Success();
    }

    @ComplexValidationTest
    public ValidationResult bcnQuantityVarValueEqualToStudyPeriod() {
        int actualStudyPeriod = analysisObject().studyPeriod() + 1;

        for (var bcn : bcnObjects()) {
            if (bcn.recur() == null)
                continue;

            var varValue = bcn.quantityVarValue();

            if (varValue != null && varValue.size() != 1 && varValue.size() != actualStudyPeriod) {
                return new ValidationResult.Failure(
                        "Quantity VarValue for BCN " + bcn.id() + " must be either null, a single value, or an array of " +
                                "values equal to the study period " + actualStudyPeriod + "."
                );
            }
        }

        return new ValidationResult.Success();
    }
}
