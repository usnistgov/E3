package gov.nist.e3.compute;

import net.jqwik.api.*;
import net.jqwik.api.Tuple.Tuple2;
import net.jqwik.api.constraints.Negative;
import net.jqwik.api.constraints.NotEmpty;
import net.jqwik.api.providers.TypeUsage;
import nz.sodium.Cell;
import org.junit.jupiter.api.Test;

import java.lang.reflect.ParameterizedType;
import java.util.List;

import static gov.nist.e3.compute.QuantityPipeline.*;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import static org.hamcrest.collection.IsIterableContainingInOrder.contains;
import static org.hamcrest.core.Is.is;
import static org.hamcrest.core.IsNot.not;
import static org.hamcrest.core.IsSame.sameInstance;

class QuantityPipelineTest {
    @Provide
    Arbitrary<Tuple2<Integer, Integer>> positiveUnequalInts() {
        return Arbitraries.integers()
                .between(0, Integer.MAX_VALUE - 1)
                .flatMap(lesser -> Arbitraries.integers()
                        .between(lesser + 1, Integer.MAX_VALUE)
                        .map(greater -> Tuple.of(lesser, greater))
                );
    }

    @Provide
    Arbitrary<Tuple2<List<Double>, Integer>> listAndInitial() {
        return Arbitraries.doubles()
                .list()
                .ofMinSize(2)
                .flatMap(list -> Arbitraries.integers()
                        .between(1, list.size() - 1)
                        .map(size -> Tuple.of(list, size))
                );
    }

    @Provide
    Arbitrary<Cell<?>> cell(TypeUsage targetType) {
        var cellType = ((ParameterizedType) targetType.getType()).getActualTypeArguments()[0];

        if (cellType.equals(Integer.class)) {
            return Arbitraries.integers().map(Cell::new);
        } else if (cellType.equals(Double.class)) {
            return Arbitraries.doubles().map(Cell::new);
        }

        return Arbitraries.of();
    }

    @Property
    void isAfterEndIsTrueIfIndexIsGreaterThanEnd(@ForAll("positiveUnequalInts") Tuple2<Integer, Integer> ints) {
        var lesser = ints.get1();
        var greater = ints.get2();

        assertThat(isAfterEnd(greater, lesser), is(true));
    }

    @Property
    void isAfterEndIsFalseIfIndexIsEqualToEnd(@ForAll int value) {
        assertThat(isAfterEnd(value, value), is(false));
    }

    @Property
    void isAfterEndIsFalseIfIndexIsLessThanEnd(@ForAll("positiveUnequalInts") Tuple2<Integer, Integer> ints) {
        var lesser = ints.get1();
        var greater = ints.get2();

        assertThat(isAfterEnd(lesser, greater), is(false));
    }

    @Property
    void isAfterEndIsFalseIfOneValueIsNegative(@ForAll @Negative int negative, @ForAll int other) {
        assertThat(isAfterEnd(negative, other), is(false));
        assertThat(isAfterEnd(other, negative), is(false));
    }

    @Property
    void isBeforeInitialIsTrueIfIndexIsLessThanInitial(@ForAll("positiveUnequalInts") Tuple2<Integer, Integer> ints) {
        var lesser = ints.get1();
        var greater = ints.get2();

        assertThat(isBeforeInitial(lesser, greater), is(true));
    }

    @Property
    void isBeforeInitialIsFalseIfIndexIsEqualToInitial(@ForAll int value) {
        assertThat(isBeforeInitial(value, value), is(false));
    }

    @Property
    void isBeforeInitialIsFalseIfIndexIsGreaterThanInitial(@ForAll("positiveUnequalInts") Tuple2<Integer, Integer> ints) {
        var lesser = ints.get1();
        var greater = ints.get2();

        assertThat(isBeforeInitial(greater, lesser), is(false));
    }

    @Property
    void isBeforeInitialIsFalseIfOneValueIsNegative(@ForAll @Negative int negative, @ForAll int other) {
        assertThat(isBeforeInitial(negative, other), is(false));
        assertThat(isBeforeInitial(other, negative), is(false));
    }

    @Test
    void isNotInIntervalIsTrueIfIndexIsNotMultipleOfInterval() {
        assertThat(isNotInInterval(2, 0, 3), is(true));
        assertThat(isNotInInterval(5, 0, 2), is(true));
    }

    @Test
    void isNotInIntervalIsTrueIfIndexMinusInitialIsNotMultipleOfInterval() {
        assertThat(isNotInInterval(5, 2, 2), is(true));
        assertThat(isNotInInterval(5, 4, 10), is(true));
    }

    @Test
    void isNotInIntervalIsFalseIfIndexIsMultipleOfInterval() {
        assertThat(isNotInInterval(5, 0, 5), is(false));
        assertThat(isNotInInterval(10, 0, 2), is(false));
        assertThat(isNotInInterval(18, 0, 3), is(false));
    }

    @Test
    void isNotInIntervalIsFalseIfIndexMinusInitialIsMultipleOfInterval() {
        assertThat(isNotInInterval(10, 5, 5), is(false));
        assertThat(isNotInInterval(6, 2, 2), is(false));
        assertThat(isNotInInterval(6, 2, 4), is(false));
    }

    @Test
    void isNotInIntervalIsFalseIfDivideByZero() {
        assertThat(isNotInInterval(0, 0, 0), is(false));
        assertThat(isNotInInterval(5, 0, 0), is(false));
        assertThat(isNotInInterval(10, 5, 0), is(false));
    }

    @Test
    void isNotInIntervalIsFalseIfIndexIsNegative() {
        assertThat(isNotInInterval(-2, 0, 2), is(false));
        assertThat(isNotInInterval(-2, 0, 3), is(false));
        assertThat(isNotInInterval(-100, 0, 6), is(false));
        assertThat(isNotInInterval(-100, 0, 5), is(false));
    }

    @Test
    void isNotInIntervalIsFalseIfInitialIsNegative() {
        assertThat(isNotInInterval(2, -2, 2), is(false));
        assertThat(isNotInInterval(2, -1, 2), is(false));
        assertThat(isNotInInterval(2, -10, 2), is(false));
        assertThat(isNotInInterval(2, -10, 3), is(false));
    }

    @Test
    void isOutsideReturnsTrueIfIsBeforeInitialIsTrue() {
        assertThat(isOutside(1, 2, 1, 1), is(true));
        assertThat(isOutside(1, 5, 0, 0), is(true));
    }

    @Test
    void isOutsideReturnsFalseIfIsBeforeInitialIsFalse() {
        assertThat(isOutside(1, 1, 1, 1), is(false));
        assertThat(isOutside(1, 1, 2, 5), is(false));
    }

    @Test
    void isOutsideReturnsTrueIfIsNotInIntervalIsTrue() {
        assertThat(isOutside(2, 1, 2, 5), is(true));
        assertThat(isOutside(2, 1, 2, 5), is(true));
    }

    @Test
    void isOutsideReturnsFalseIfIsNotInIntervalIsFalse() {
        assertThat(isOutside(2, 2, 3, 5), is(false));
        assertThat(isOutside(2, 2, 6, 3), is(false));
    }

    @Test
    void isOutsideReturnsTrueIfIsAfterEndIsTrue() {
        assertThat(isOutside(5, 1, 1, 3), is(true));
        assertThat(isOutside(5, 1, 2, 2), is(true));
    }

    @Test
    void isOutsideReturnsFalseIfIsAfterEndIsFalse() {
        assertThat(isOutside(5, 1, 1, 10), is(false));
        assertThat(isOutside(5, 1, 2, 6), is(false));
    }

    @Property
    void replaceOutsideReturnsSameSizeListProperty(@ForAll List<Double> values, @ForAll int initial, @ForAll int interval, @ForAll int end) {
        assertThat(replaceOutside(values, initial, interval, end), hasSize(values.size()));
    }

    @Property
    void replaceOutsideDoesNotReturnSameListReference(@ForAll List<Double> values, @ForAll int initial, @ForAll int interval, @ForAll int end) {
        assertThat(replaceOutside(values, initial, interval, end), is(not(sameInstance(values))));
    }

    @Property
    void replaceOutsideDoesNotAlterListIfNonAreOutside(@ForAll @NotEmpty List<Double> values) {
        assertThat(replaceOutside(values, 0, 1, values.size()), contains(values.toArray()));
    }

    @Property
    void replaceOutsideDoesNotReplaceAnyValueIfInitialIsZero(@ForAll @NotEmpty List<Double> values) {
        assertThat(replaceOutside(values, 0, 1, values.size()), contains(values.toArray()));
    }

    @Property
    void replaceOutsideReplacesValuesBeforeBeginning(@ForAll("listAndInitial") Tuple2<List<Double>, Integer> tuple) {
        var values = tuple.get1();
        int initial = tuple.get2();

        var result = replaceOutside(values, initial, 1, values.size());

        var beginning = result.subList(0, initial);
        var end = result.subList(initial, values.size());

        assertThat(beginning, everyItem(is(equalTo(0.0))));
        assertThat(end, contains(values.subList(initial, values.size()).toArray()));
    }

/*    @Property
    void constructorDefinesOutputCell(
            @ForAll("cell") Cell<Double> quantity,
            @ForAll List<Double> values,
            @ForAll VarRate varRate,
            @ForAll("cell") Cell<Integer> initialOccurrence,
            @ForAll("cell") Cell<Integer> interval,
            @ForAll("cell") Cell<Integer> end
    ) {
        var pipeline = new QuantityPipeline(
                quantity,
                new Cell<>(values),
                new Cell<>(varRate),
                initialOccurrence,
                interval,
                end
        );

        assertThat(pipeline.cQuantities, is(notNullValue()));
    }*/

    @Property
    void testPushingNewCell(@ForAll("cell") Cell<Double> doubleCell) {
        System.out.println(doubleCell);
    }
}