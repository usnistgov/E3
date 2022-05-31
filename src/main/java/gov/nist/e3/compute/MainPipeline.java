package gov.nist.e3.compute;

import gov.nist.e3.Config;
import gov.nist.e3.objects.OptionalKey;
import gov.nist.e3.objects.input.*;
import gov.nist.e3.objects.output.*;
import gov.nist.e3.tree.Tree;
import gov.nist.e3.util.CellUtils;
import gov.nist.e3.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import nz.sodium.Transaction;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

public class MainPipeline {
    private static final Logger log = LoggerFactory.getLogger(MainPipeline.class);

    private Cell<SensitivityPipeline> sensitivityPipeline;
    private Cell<List<RequiredCashflow>> requiredCashflows;
    private Cell<List<OptionalCashflow>> optionalCashflows;
    private Cell<List<MeasureSummary>> measureSummaries;
    private Cell<UncertaintyPipeline> uncertaintyPipeline;

    public final Analysis defaultAnalysis = new Analysis(
            AnalysisType.OTHER,
            null,
            null,
            11,
            null,
            null,
            false,
            0.0,
            0.03,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            new Location("a", "b", "C", "d"),
            1,
            0
    );

    public MainPipeline(Stream<Input> sInput) {
        Transaction.runVoid(() -> define(sInput));
    }

    public void define(Stream<Input> sInput) {
        var cBcn = sInput.map(Input::bcnObjects).hold(List.of()).map(this::createIdToBcnMap);
        var cAlternatives = sInput.map(Input::alternativeObjects).hold(List.of());
        var cAnalysis = sInput.map(Input::analysisObject).hold(defaultAnalysis);
        var cAnalysisCell = cAnalysis.map(Analysis::toCell);

        var cOutputTypes = sInput.map(Input::analysisObject).hold(defaultAnalysis).map(Analysis::outputObjects);
        var cOutputDependencies = cOutputTypes.map(Config.E3_DEPENDENCY_GRAPH::getAll);

        var cStudyPeriod = cAnalysisCell.map(AnalysisCell::cStudyPeriod);
        var cTimestepComp = cAnalysis.map(Analysis::timestepComp);

        var cDiscountRate = Cell.switchC(
                cAnalysis.map(Analysis::outputReal).map(real -> Boolean.TRUE.equals(real) ? cAnalysisCell.map(AnalysisCell::cDiscountRateReal) : cAnalysisCell.map(AnalysisCell::cDiscountRateNominal))
        );
        var cAlternativeIndices = cAlternatives.map(this::alternativeGroupIds);
        var cAlternativeIDs = cAlternativeIndices.map(Map::keySet);
        var cOptionalIndices = cBcn.map(this::optionalGroupIndices);
        var cBaselineId = Cell.switchC(cAnalysisCell.map(AnalysisCell::cBaseAlternative));

        var cQuantityPipelines = cAnalysisCell.lift(cBcn, this::createQuantityPipelines);
        var cValuePipelines = cBcn.lift(cQuantityPipelines, this::createValuePipelines);
        var cResidualValuePipeline = cAnalysisCell.lift(cBcn, cValuePipelines, this::createResidualValuePipelines);
        var cDiscountPipelines = cDiscountRate.lift(cResidualValuePipeline, cTimestepComp, this::createDiscountPipelines);

        var cRequiredCashflowPipelines = cAlternativeIndices.lift(
                cBcn,
                cResidualValuePipeline,
                cDiscountPipelines,
                cStudyPeriod,
                this::createRequiredCashflowPipelines
        );
        var cOptionalCashflowPipelines = cOptionalIndices.lift(
                cBcn, cQuantityPipelines, cDiscountPipelines, this::createOptionalCashflowPipelines
        );

        //TODO: make sure gated cells do not compute if they are not needed

        var cRequiredCashflows = CellUtils.gate(
                cOutputDependencies,
                types -> types.contains(OutputType.REQUIRED),
                () -> Cell.switchC(
                        cRequiredCashflowPipelines.map(Map::values)
                                .map(list -> list.stream().map(p -> p.cRequiredCashflow).toList())
                                .map(CellUtils::sequence)
                )
        );
        var cOptionalCashflows = CellUtils.gate(
                cOutputDependencies,
                types -> types.contains(OutputType.OPTIONAL),
                () -> Cell.switchC(
                        cOptionalCashflowPipelines.map(Map::values)
                                .map(list -> list.stream().map(p -> p.cOptionalCashflows).toList())
                                .map(CellUtils::sequence)
                )
        );

        var cAlternativeGroupedOptionals = cOptionalCashflowPipelines.map(
                this::alternativeGroupedOptionals
        );
        var cBaselineMeasureSummaryPipeline = cBaselineId.lift(
                cAnalysisCell, cRequiredCashflowPipelines, cAlternativeGroupedOptionals, this::createBaselineMeasureSummary
        );
        var cMeasureSummaryPipelines = cBaselineId.lift(
                cBaselineMeasureSummaryPipeline,
                cAnalysisCell,
                cRequiredCashflowPipelines,
                cAlternativeGroupedOptionals,
                this::createNonBaselineMeasureSummaries
        );

        var cMeasureSummaries = CellUtils.gate(
                cOutputDependencies,
                types -> types.contains(OutputType.MEASURES),
                () -> Cell.switchC(
                        cMeasureSummaryPipelines.map(Map::values)
                                .map(list -> list.stream().map(p -> p.cMeasureSummary).toList())
                                .map(CellUtils::sequence)
                )
        );

        var cSensitivityPipelines = CellUtils.gate(
                cOutputDependencies,
                types -> types.contains(OutputType.SENSITIVITY),
                () -> createSensitivityPipeline(sInput, cMeasureSummaryPipelines)
        );

        var cUncertaintyPipelines = CellUtils.gate(
                cOutputDependencies,
                types -> types.contains(OutputType.UNCERTAINTY),
                () -> createUncertaintyPipeline(sInput, cMeasureSummaryPipelines, cBcn, cAlternativeIDs)
        );

        requiredCashflows = CellUtils.gate(
                cOutputTypes, t -> t != null && t.contains(OutputType.REQUIRED), () -> cRequiredCashflows
        );
        optionalCashflows = CellUtils.gate(
                cOutputTypes, t -> t != null && t.contains(OutputType.OPTIONAL), () -> cOptionalCashflows
        );
        measureSummaries = CellUtils.gate(
                cOutputTypes, t -> t != null && t.contains(OutputType.MEASURES), () -> cMeasureSummaries
        );
        sensitivityPipeline = CellUtils.gate(
                cOutputTypes, t -> t != null && t.contains(OutputType.SENSITIVITY), () -> cSensitivityPipelines
        );
        uncertaintyPipeline = CellUtils.gate(
                cOutputTypes, t -> t != null && t.contains(OutputType.UNCERTAINTY), () -> cUncertaintyPipelines
        );
    }

    public Cell<UncertaintyPipeline> createUncertaintyPipeline(
            Stream<Input> sInput,
            Cell<Map<Integer, MeasureSummaryPipeline>> cMeasureSummaryPipelines,
            Cell<Map<Integer, Bcn>> bcns,
            Cell<Set<Integer>> altIDs
    ) {
        var cUncertainty = sInput.map(Input::uncertainty).hold(List.of());
        var cTree = sInput.map(Input::toTree).hold(Tree.create());

        return cUncertainty.lift(cTree, cMeasureSummaryPipelines, bcns, altIDs, UncertaintyPipeline::new);
    }

    public Cell<SensitivityPipeline> createSensitivityPipeline(
            Stream<Input> sInput,
            Cell<Map<Integer, MeasureSummaryPipeline>> cMeasureSummaryPipelines
    ) {
        var cSensitivity = sInput.map(Input::sensitivityObjects).hold(List.of());
        var cTree = sInput.map(Input::toTree).hold(Tree.create());

        return cSensitivity.lift(cTree, cMeasureSummaryPipelines, SensitivityPipeline::new);
    }

    public Map<Integer, QuantityPipeline> createQuantityPipelines(AnalysisCell analysisCell, Map<Integer, Bcn> bcns) {
        var result = new HashMap<Integer, QuantityPipeline>();

        for (var entry : bcns.entrySet()) {
            var bcn = entry.getValue();

            var cEnd = bcn.recur() == null ? new Cell<Integer>(null) : bcn.recur().cEnd();

            result.put(entry.getKey(), new QuantityPipeline(
                    bcn.cQuantity(),
                    bcn.quantityVarValue(),
                    bcn.quantityVarRate(),
                    bcn.cInitialOccurrence(),
                    bcn.recur() != null ? bcn.recur().cInterval() : null,
                    cEnd,
                    analysisCell.cStudyPeriod(),
                    bcn.recur()
            ));
        }

        return result;
    }

    public Map<Integer, ValuePipeline> createValuePipelines(
            Map<Integer, Bcn> bcns,
            Map<Integer, QuantityPipeline> quantityPipelines
    ) {
        var num = bcns.size();

        if (quantityPipelines.size() != num)
            throw new IllegalArgumentException("Number of quantity pipelines must be equal to number of BCNs");

        var result = new HashMap<Integer, ValuePipeline>();

        for (var entry : bcns.entrySet()) {
            var id = entry.getKey();
            var bcn = entry.getValue();
            var quantityPipeline = quantityPipelines.get(id);

            var varValue = bcn.recur() == null ? null : bcn.recur().varValue();
            var varRate = bcn.recur() == null ? null : bcn.recur().varRate();

            result.put(id, new ValuePipeline(quantityPipeline.cQuantities, bcn.cQuantityValue(), varValue, varRate));
        }

        return result;
    }

    public Map<Integer, ResidualValuePipeline> createResidualValuePipelines(
            AnalysisCell analysis,
            Map<Integer, Bcn> bcns,
            Map<Integer, ValuePipeline> valuePipelines
    ) {
        var num = bcns.size();

        if (valuePipelines.size() != num)
            throw new IllegalArgumentException("Number of value pipelines must be equal to number of BCNs");

        var result = new HashMap<Integer, ResidualValuePipeline>();

        for (var entry : bcns.entrySet()) {
            var id = entry.getKey();
            var bcn = entry.getValue();
            var valuePipeline = valuePipelines.get(id);

            result.put(id, new ResidualValuePipeline(
                    valuePipeline.cValues,
                    analysis.cStudyPeriod(),
                    bcn.cLife(),
                    bcn.cInitialOccurrence(),
                    bcn.recur(),
                    bcn.residualValue(),
                    bcn.residualValueOnly()
            ));
        }

        return result;
    }

    public Map<Integer, DiscountedPipeline> createDiscountPipelines(
            Cell<Double> rate,
            Map<Integer, ResidualValuePipeline> residualValuePipelines,
            TimestepComp timestepComp
    ) {
        var result = new HashMap<Integer, DiscountedPipeline>();

        for (var entry : residualValuePipelines.entrySet()) {
            result.put(entry.getKey(), new DiscountedPipeline(
                    entry.getValue().cValuesWithResidual, rate, timestepComp
            ));
        }

        return result;
    }

    public Map<Integer, RequiredCashflowPipeline> createRequiredCashflowPipelines(
            Map<Integer, List<Integer>> groups,
            Map<Integer, Bcn> bcns,
            Map<Integer, ResidualValuePipeline> residualValuePipeline,
            Map<Integer, DiscountedPipeline> discountedPipelines,
            Cell<Integer> cStudyPeriod
    ) {
        var result = new HashMap<Integer, RequiredCashflowPipeline>();

        for (var groupEntry : groups.entrySet()) {
            var alternativeId = groupEntry.getKey();
            var ids = groupEntry.getValue();

            var groupBcns = Util.getIndices(bcns, ids);
            var groupValues = Util.getIndices(residualValuePipeline, ids);
            var groupDiscounts = Util.getIndices(discountedPipelines, ids);

            result.put(alternativeId, new RequiredCashflowPipeline(
                    alternativeId,
                    groupBcns,
                    groupValues,
                    groupDiscounts,
                    cStudyPeriod
            ));
        }

        return result;
    }

    public Map<OptionalKey, OptionalCashflowPipeline> createOptionalCashflowPipelines(
            Map<OptionalKey, List<Integer>> indices,
            Map<Integer, Bcn> bcns,
            Map<Integer, QuantityPipeline> quantityPipelines,
            Map<Integer, DiscountedPipeline> discountedPipelines
    ) {
        var result = new HashMap<OptionalKey, OptionalCashflowPipeline>();

        for (var entry : indices.entrySet()) {
            var key = entry.getKey();
            var ids = entry.getValue();

            result.put(key, new OptionalCashflowPipeline(
                    key.altId(),
                    key.tag(),
                    Util.getIndices(bcns, ids),
                    Util.getIndices(quantityPipelines, ids),
                    Util.getIndices(discountedPipelines, ids)
            ));
        }

        return result;
    }

    public Map<OptionalKey, List<Integer>> optionalGroupIndices(Map<Integer, Bcn> bcns) {
        return Util.nestedGroup(OptionalKey::new, Bcn::altIds, Bcn::tags, Bcn::id, bcns.values());
    }

    public Map<Integer, List<Integer>> alternativeGroupIds(List<Alternative> alternatives) {
        return alternatives.stream().collect(Collectors.toMap(Alternative::id, Alternative::bcns));
    }

    public Map<Integer, Bcn> createIdToBcnMap(List<Bcn> bcn) {
        return bcn.stream().collect(Collectors.toMap(Bcn::id, b -> b));
    }

    public Map<Integer, List<OptionalCashflowPipeline>> alternativeGroupedOptionals(Map<OptionalKey, OptionalCashflowPipeline> pipelines) {
        var result = new HashMap<Integer, List<OptionalCashflowPipeline>>();

        for (var entry : pipelines.entrySet()) {
            var altId = entry.getKey().altId();
            var pipeline = entry.getValue();

            result.compute(altId, (id, current) -> {
                var list = current == null ? new ArrayList<OptionalCashflowPipeline>() : current;
                list.add(pipeline);
                return list;
            });
        }

        return result;
    }

    public MeasureSummaryPipeline createBaselineMeasureSummary(
            int baselineId,
            AnalysisCell analysis,
            Map<Integer, RequiredCashflowPipeline> requiredCashflowPipelines,
            Map<Integer, List<OptionalCashflowPipeline>> optionalCashflowPipelines
    ) {
        log.trace("createBaselineMeasureSummary");

        if (!requiredCashflowPipelines.containsKey(baselineId))
            return null;

        var baselineRequired = requiredCashflowPipelines.get(baselineId);
        var baselineOptionals = optionalCashflowPipelines.get(baselineId);

        return new MeasureSummaryPipeline(
                analysis.cReinvestRate(),
                analysis.cStudyPeriod(),
                analysis.cMarr(),
                baselineRequired,
                baselineOptionals,
                null,
                null
        );
    }

    public Map<Integer, MeasureSummaryPipeline> createNonBaselineMeasureSummaries(
            int baselineId,
            @Nullable MeasureSummaryPipeline baselineMeasure,
            AnalysisCell analysis,
            Map<Integer, RequiredCashflowPipeline> requiredCashflowPipelines,
            Map<Integer, List<OptionalCashflowPipeline>> optionalCashflowPipelines
    ) {
        log.trace("createNonBaselineMeasureSummaries");

        if (!requiredCashflowPipelines.containsKey(baselineId) || baselineMeasure == null)
            return new HashMap<>();

        var result = new HashMap<Integer, MeasureSummaryPipeline>();
        var baselineRequiredCashflow = requiredCashflowPipelines.get(baselineId);

        result.put(baselineId, baselineMeasure);

        for (var entry : requiredCashflowPipelines.entrySet()) {
            var alternative = entry.getKey();

            if (alternative == baselineId)
                continue;

            var baselineRequired = requiredCashflowPipelines.get(alternative);
            var baselineOptionals = optionalCashflowPipelines.get(alternative);

            result.put(alternative, new MeasureSummaryPipeline(
                    analysis.cReinvestRate(),
                    analysis.cStudyPeriod(),
                    analysis.cMarr(),
                    baselineRequired,
                    baselineOptionals,
                    baselineMeasure,
                    baselineRequiredCashflow
            ));
        }

        return result;
    }

    public List<SensitivitySummary> sensitivity() {
        var sample = sensitivityPipeline.sample();
        return sample == null ? null : sample.analyze();
    }

    public List<UncertaintySummary> uncertainty() {
        var sample = uncertaintyPipeline.sample();
        return sample == null ? null : sample.analyze();
    }

    public List<RequiredCashflow> required() {
        return requiredCashflows.sample();
    }

    public List<OptionalCashflow> optional() {
        return optionalCashflows.sample();
    }

    public List<MeasureSummary> measures() {
        return measureSummaries.sample();
    }
}
