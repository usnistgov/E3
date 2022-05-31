package gov.nist.e3.compute;

import gov.nist.e3.Config;
import gov.nist.e3.objects.input.Sensitivity;
import gov.nist.e3.objects.input.SensitivityDiffType;
import gov.nist.e3.objects.output.MeasureSummary;
import gov.nist.e3.objects.output.SensitivitySummary;
import gov.nist.e3.tree.Tree;
import nz.sodium.Cell;
import nz.sodium.CellSink;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SensitivityPipeline {
    private final List<Sensitivity> sensitivities;
    private final Tree<String, CellSink<? extends Number>> cellTree;
    private final Map<Integer, MeasureSummaryPipeline> measureSummaryPipelines;

    public SensitivityPipeline(
            List<Sensitivity> sensitivities,
            Tree<String, CellSink<? extends Number>> cellTree,
            Map<Integer, MeasureSummaryPipeline> measureSummaries
    ) {
        this.sensitivities = sensitivities;
        this.cellTree = cellTree;
        this.measureSummaryPipelines = measureSummaries;
    }

    public List<SensitivitySummary> analyze() {
        var output = new ArrayList<SensitivitySummary>(sensitivities.size());

        for(var sensitivity: sensitivities) {
            var summaries = new HashMap<Cell<MeasureSummary>, SensitivitySummary>();
            for(var altId: sensitivity.altIds()) {
                var cMeasureSummary = measureSummaryPipelines.get(altId).cMeasureSummary;
                summaries.put(cMeasureSummary, SensitivitySummary.of(sensitivity.id(), cMeasureSummary.sample()));
            }

            var path = sensitivity.variable().split(Config.TREE_PATTERN);
            var cell = (CellSink<Number>) cellTree.get(path);
            var original = cell.sample();

            switch (sensitivity.diffType()) {
                case PERCENT, POSITIVE_PERCENT, NEGATIVE_PERCENT -> runPercent(sensitivity, cell, summaries);
                case GROSS, POSITIVE_GROSS, NEGATIVE_GROSS -> runGross(sensitivity, cell, summaries);
            }

            // Reset value to original.
            cell.send(original);
            output.addAll(summaries.values());
        }

        return output;
    }

    private void runGross(
            Sensitivity sensitivity,
            CellSink<Number> cell,
            HashMap<Cell<MeasureSummary>, SensitivitySummary> summaries
    ) {
        var diffType = sensitivity.diffType();
        var original = cell.sample();

        // Send upper value.
        if(diffType == SensitivityDiffType.GROSS || diffType == SensitivityDiffType.POSITIVE_GROSS) {
            var upper = getUpperGross(original, sensitivity.diffValue());

            cell.send(upper);
            summaries.forEach((cMeasure, summary) -> summary.addMeasureSummary(cMeasure.sample()));
        }

        // Send lower value.
        if(diffType == SensitivityDiffType.GROSS || diffType == SensitivityDiffType.NEGATIVE_GROSS) {
            var lower = getLowerGross(original, sensitivity.diffValue());

            cell.send(lower);
            summaries.forEach((cMeasure, summary) -> summary.addMeasureSummary(cMeasure.sample()));
        }
    }

    private void runPercent(
            Sensitivity sensitivity,
            CellSink<Number> cell,
            HashMap<Cell<MeasureSummary>, SensitivitySummary> summaries
    ) {
        var diffType = sensitivity.diffType();
        var original = cell.sample();

        // Send upper value.
        if(diffType == SensitivityDiffType.PERCENT || diffType == SensitivityDiffType.POSITIVE_PERCENT) {
            var upper = getUpperPercent(original, sensitivity.diffValue());

            cell.send(upper);
            summaries.forEach((cMeasure, summary) -> summary.addMeasureSummary(cMeasure.sample()));
        }

        // Send lower value.
        if(diffType == SensitivityDiffType.PERCENT || diffType == SensitivityDiffType.NEGATIVE_PERCENT) {
            var lower = getLowerPercent(original, sensitivity.diffValue());

            cell.send(lower);
            summaries.forEach((cMeasure, summary) -> summary.addMeasureSummary(cMeasure.sample()));
        }
    }

    public Number getUpperPercent(Number original, double diffValue) {
        if(original instanceof Double originalDouble)
            return originalDouble * (1.0 + diffValue);
        else if(original instanceof Integer originalInteger)
            return originalInteger * (1 + (int) diffValue);

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }

    public Number getLowerPercent(Number original, double diffValue) {
        if(original instanceof Double originalDouble)
            return originalDouble * (1.0 - diffValue);
        else if(original instanceof Integer originalInteger)
            return originalInteger * (1 - (int) diffValue);

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }

    public Number getUpperGross(Number original, double diffValue) {
        if(original instanceof Double originalDouble)
            return originalDouble + diffValue;
        else if(original instanceof Integer originalInteger)
            return originalInteger + (int) diffValue;

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }

    public Number getLowerGross(Number original, double diffValue) {
        if(original instanceof Double originalDouble)
            return originalDouble - diffValue;
        else if(original instanceof Integer originalInteger)
            return originalInteger - (int) diffValue;

        throw new IllegalArgumentException("Number must be double or integer. Was: " + original.getClass());
    }
}
