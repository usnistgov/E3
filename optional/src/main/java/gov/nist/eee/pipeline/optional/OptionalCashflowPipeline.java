package gov.nist.eee.pipeline.optional;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.input.Bcn;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.pipeline.discounted.DiscountedPipeline;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.pipeline.value.ValuePipeline;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import nz.sodium.Cell;
import nz.sodium.Stream;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Function;

@Pipeline(name = "optional", dependencies = {QuantityPipeline.class, DiscountedPipeline.class, ValuePipeline.class})
@OutputMapper(OptionalOutputMapper.class)
public class OptionalCashflowPipeline
        extends CellPipeline<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception>>
        implements IWithDependency {
    private static final Logger logger = LoggerFactory.getLogger(OptionalCashflowPipeline.class);
    private Cell<Map<OptionalKey, List<Bcn>>> cBcnGroups;
    private Cell<Result<Map<OptionalKey, List<Cell<List<Double>>>>, E3Exception>> cQuantityGroups;
    private Cell<Result<Map<OptionalKey, List<Cell<List<Double>>>>, E3Exception>> cDiscountedGroups;
    private Cell<Result<Map<OptionalKey, List<Cell<List<Double>>>>, E3Exception>> cNonDiscountGroups;

    @Override
    public void setup(Stream<Input> sInput) {
        logger.trace("Setting up optional cashflow pipeline.");

        var cBcns = sInput.map(Input::bcnObjects).hold(List.of());

        var cBcnAltIDs = sInput.map(Input::alternativeObjects).hold(List.of()).map(Util::groupByBcn);
        cBcnGroups = cBcnAltIDs.lift(cBcns, OptionalCashflowPipeline::getBcnGroups);
    }

    @Override
    @SuppressWarnings("unchecked")
    public void setupDependency(DependencyParameters parameters) {
        logger.trace("Setting up dependencies for optional cashflow pipeline. " + parameters);

        var cQuantities = (Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>) parameters.get(QuantityPipeline.class);
        cQuantityGroups = cQuantities.lift(cBcnGroups, (quantity, groups) -> quantity.map(q -> filterByKey(q, groups)));

        var cDiscounted = (Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>) parameters.get(DiscountedPipeline.class);
        cDiscountedGroups = cDiscounted.lift(cBcnGroups, (discounted, groups) -> discounted.map(d -> filterByKey(d, groups)));

        var cValues = (Cell<Result<Map<Integer, Cell<List<Double>>>, E3Exception>>) parameters.get(ValuePipeline.class);
        cNonDiscountGroups = cValues.lift(cBcnGroups, (values, groups) -> values.map(v -> filterByKey(v, groups)));
    }

    public <T> Map<OptionalKey, List<T>> filterByKey(Map<Integer, T> value, Map<OptionalKey, List<Bcn>> groups) {
        var result = new HashMap<OptionalKey, List<T>>();

        for (var entry : groups.entrySet()) {
            var key = entry.getKey();
            var bcns = entry.getValue();

            result.put(key, bcns.stream().map(bcn -> value.get(bcn.id())).toList());
        }

        return result;
    }

    @Override
    public Cell<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception>> define() {
        logger.trace("Defining optional cashflow pipeline.");

        return cBcnGroups.lift(
                cQuantityGroups,
                cDiscountedGroups,
                cNonDiscountGroups,
                (bcnGroups, rquantityGroups, rdiscountedGroups, rNonDiscountedGroups) -> rquantityGroups.flatMap(quantityGroups -> rdiscountedGroups.flatMap(discountedGroups -> rNonDiscountedGroups.map(nonDiscountGroups -> {
                    var result = new HashMap<OptionalKey, Cell<OptionalCashflow>>();

                    for (var entry : bcnGroups.entrySet()) {
                        var key = entry.getKey();
                        var bcns = entry.getValue();

                        var altID = key.altId();
                        var tag = key.tag();
                        var unit = bcns.get(0).quantityUnit();

                        var cQuantitySum = CellUtils.mergeList(
                                Util::elementwiseAdd, quantityGroups.get(key)
                        );
                        var cDiscountedSum = CellUtils.mergeList(
                                Util::elementwiseAdd, discountedGroups.get(key)
                        );
                        var cNonDiscountedSum = CellUtils.mergeList(
                                Util::elementwiseAdd, nonDiscountGroups.get(key)
                        );

                        var cOptionalCashflow = cQuantitySum.lift(
                                cDiscountedSum,
                                cNonDiscountedSum,
                                (quantitySum, discountedSum, nonDiscountedSum) ->
                                        new OptionalCashflow(altID, tag, discountedSum, nonDiscountedSum, quantitySum, unit)
                        );

                        result.put(key, cOptionalCashflow);
                    }


                    return result;
                })))
        );
    }

    public static <K, A, B, C, D> Map<K, List<D>> nestedGroup(
            BiFunction<B, C, K> keyConstructor,
            Function<A, List<B>> mapper1,
            Function<A, List<C>> mapper2,
            Function<A, D> valueMapper,
            Iterable<A> values
    ) {
        var result = new HashMap<K, List<D>>();

        for (var value : values) {
            for (var b : mapper1.apply(value)) {
                for (var c : mapper2.apply(value)) {
                    var key = keyConstructor.apply(b, c);

                    result.compute(key, (k, v) -> {
                        var list = v == null ? new ArrayList<D>() : v;
                        list.add(valueMapper.apply(value));
                        return list;
                    });
                }
            }
        }

        return result;
    }

    public static <K, A, B, C> Map<K, List<A>> nestedGroup(
            BiFunction<B, C, K> keyConstructor,
            Function<A, List<B>> mapper1,
            Function<A, List<C>> mapper2,
            Iterable<A> values
    ) {
        return nestedGroup(keyConstructor, mapper1, mapper2, v -> v, values);
    }

    public static <A, B> List<B> getIndices(Map<A, B> map, List<A> keys) {
        var result = new ArrayList<B>(keys.size());

        for (var key : keys) {
            if (!map.containsKey(key))
                continue;

            result.add(map.get(key));
        }

        return result;
    }

    @NotNull
    private static HashMap<OptionalKey, List<Bcn>> getBcnGroups(Map<Integer, Set<Integer>> altIDs, List<Bcn> bcns) {
        var result = new HashMap<OptionalKey, List<Bcn>>();

        for (var bcn : bcns) {
            for (var altID : altIDs.get(bcn.id())) {
                if(bcn.tags() == null)
                    continue;

                for(var tag: bcn.tags()) {
                    var key = new OptionalKey(altID, tag);

                    if(!result.containsKey(key))
                        result.put(key, new ArrayList<>());

                    result.get(key).add(bcn);
                }
            }
        }

        return result;
    }
}
