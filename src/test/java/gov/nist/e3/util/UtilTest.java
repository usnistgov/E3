package gov.nist.e3.util;

import gov.nist.e3.objects.input.VarRate;
import net.jqwik.api.*;
import net.jqwik.api.Tuple.Tuple2;
import net.jqwik.api.constraints.NotEmpty;
import org.junit.jupiter.api.Test;

import java.util.List;

import static gov.nist.e3.util.Util.*;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

class UtilTest {
    @Provide
    Arbitrary<Tuple2<List<Integer>, List<Integer>>> sameSizeLists() {
        return Arbitraries.integers()
                .list()
                .flatMap(list1 -> Arbitraries.integers()
                        .list()
                        .ofSize(list1.size())
                        .map(list2 -> Tuple.of(list1, list2))
                );
    }

    @Property
    void multiplierReturnsListOfSameSize(@ForAll List<Double> values, @ForAll double multiplier) {
        assertThat(multiplier(values, multiplier), hasSize(values.size()));
    }

    @Property
    void multiplierMultipliesEachValue(@ForAll List<Double> values, @ForAll double multiplier) {
        var result = multiplier(values, multiplier);

        for (int i = 0; i < values.size(); i++) {
            var expected = values.get(i);
            var actual = result.get(i);

            assertThat(actual, is(equalTo(expected * multiplier)));
        }
    }

    @Property
    void mapWithVarRateReturnsSameValuesIfRateIsYearByYear(@ForAll @NotEmpty List<Double> values) {
        assertThat(mapWithVarRate(values, VarRate.YEAR_BY_YEAR), contains(values.toArray()));
    }

    @Test
    void mapWithVarRateReturnsEmptyListIfInputIsEmpty() {
        assertThat(mapWithVarRate(List.of(), VarRate.YEAR_BY_YEAR), hasSize(0));
        assertThat(mapWithVarRate(List.of(), VarRate.PERCENT_DELTA), hasSize(0));
    }

    @Property
    void scanReturnsListWithSameSize(@ForAll List<Integer> ints) {
        assertThat(scan(ints, 0, Integer::sum), hasSize(ints.size()));
    }

    @Property
    void scanDoesNotReturnSameList(@ForAll List<Integer> ints) {
        assertThat(scan(ints, 0, Integer::sum), is(not(sameInstance(ints))));
    }

    @Test
    void scanAppliesFunction() {
        var result = scan(List.of(1, 2, 3, 4, 5), 0, Integer::sum);

        assertThat(result, contains(1, 3, 6, 10, 15));
    }

    @Property
    void elementwiseReturnsListOfSameSize(@ForAll("sameSizeLists") Tuple2<List<Integer>, List<Integer>> lists) {
        var list1 = lists.get1();
        var list2 = lists.get2();


        var result = elementwise(list1, list2, Integer::sum);

        assertThat(result, hasSize(list1.size()));
        assertThat(result, hasSize(list2.size()));
    }

    @Property
    void elementwiseReturnsDifferentList(@ForAll("sameSizeLists") Tuple2<List<Integer>, List<Integer>> lists) {
        var list1 = lists.get1();
        var list2 = lists.get2();

        var result = elementwise(list1, list2, Integer::sum);

        assertThat(result, is(not(sameInstance(list1))));
        assertThat(result, is(not(sameInstance(list2))));
    }
}