package gov.nist.eee.util;

import gov.nist.eee.util.function.QuadFunction;
import gov.nist.eee.util.function.TriFunction;
import net.jqwik.api.Example;
import net.jqwik.api.ForAll;
import net.jqwik.api.Group;
import net.jqwik.api.Property;
import net.jqwik.api.constraints.NotEmpty;
import net.jqwik.api.constraints.Scale;
import org.mockito.Mockito;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.closeTo;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.verify;

class UtilTest {

    @Group
    class Elementwise {
        /**
         * {@link Util#elementwise(List, List, BiFunction)} with the identity function returns original list.
         */
/*        @Property
        void identity(@ForAll List<Double> left, @ForAll List<Double> right) {
            assertEquals(left, Util.elementwise(left, right, (x, y) -> x));
            assertEquals(right, Util.elementwise(left, right, (x, y) -> y));
        }*/
    }

    @Group
    class Compound {
        /**
         * {@link Util#compound(List)} should return a list that is the same size as the input list.
         */
        @Property
        void resultIsSameSize(@ForAll List<Double> values) {
            assertEquals(values.size(), Util.compound(values).size());
        }

        /**
         * {@link Util#compound(List)} should return a list with the first value being equal to the original plus 1.0.
         */
        @Property
        void firstValueIsTheSame(@ForAll @NotEmpty List<Double> values) {
            assertEquals(values.get(0) + 1.0, Util.compound(values).get(0));
        }

        /**
         * {@link Util#compound(List)} should not occur for empty list.
         */
        @Example
        void emptyList() {
            assertTrue(Util.compound(List.of()).isEmpty());
        }
    }

    @Group
    class Sum {
        /**
         * {@link Util#sum(List)} returns the addition of the elements in a list.
         */
        @Example
        void sumReturnsAdditionOfElements() {
            var expected = 6.0;
            double result = Util.sum(List.of(1.0, 2.0, 3.0));

            if (!Double.isInfinite(result))
                assertThat(result, closeTo(expected, 0.0001));
        }

        /**
         * {@link Util#sum(List)} should throw an {@link ArithmeticException} when the result is {@link Double#NaN}.
         */
        @Example
        void nanThrowsException() {
            assertThrows(ArithmeticException.class, () -> Util.sum(List.of(1.0, 2.0, Double.NaN)));
        }

        /**
         * {@link Util#sum(List)} returns {@link Double#POSITIVE_INFINITY} when two large numbers are summed.
         */
        @Example
        void sumReturnsInfinity() {
            assertEquals(Double.POSITIVE_INFINITY, Util.sum(List.of(Double.MAX_VALUE, Double.MAX_VALUE)));
        }
    }

    @Group
    class CombineMap {
        /**
         * {@link Util#combineMap(Map, Map, BiFunction)} should call function to combine values.
         */
        @Example
        @SuppressWarnings("unchecked")
        void callsFunction() {
            var map1 = Map.of(1, "a", 2, "b");
            var map2 = Map.of(1, "c", 2, "d");
            var map3 = Map.of(1, "e", 2, "f");
            var map4 = Map.of(1, "g", 2, "h");

            var biMock = Mockito.mock(BiFunction.class);
            var triMock = Mockito.mock(TriFunction.class);
            var quadMock = Mockito.mock(QuadFunction.class);

            Util.combineMap(map1, map2, biMock);
            Util.combineMap(map1, map2, map3, triMock);
            Util.combineMap(map1, map2, map3, map4, quadMock);

            verify(biMock).apply("a", "c");
            verify(biMock).apply("b", "d");

            verify(triMock).apply("a", "c", "e");
            verify(triMock).apply("b", "d", "f");

            verify(quadMock).apply("a", "c", "e", "g");
            verify(quadMock).apply("b", "d", "f", "h");
        }

        /**
         * {@link Util#combineMap(Map, Map, BiFunction)} should have the same keys as the first parameter map.
         */
        @Example
        void sameKeys() {
            var map1 = Map.of(1, "a", 2, "b");
            var map2 = Map.of(1, "c", 2, "d");
            var map3 = Map.of(1, "e", 2, "f");
            var map4 = Map.of(1, "g", 2, "h");

            var result1 = Util.combineMap(map1, map2, String::concat);
            var result2 = Util.combineMap(map1, map2, map3, (x, y, z) -> x + y + z);
            var result3 = Util.combineMap(map1, map2, map3, map4, (x, y, z, w) -> x + y + z + w);

            assertEquals(map1.size(), result1.size());
            assertEquals(map2.size(), result1.size());
            assertEquals(map1.keySet(), result1.keySet());
            assertEquals(map2.keySet(), result1.keySet());

            assertEquals(map1.size(), result2.size());
            assertEquals(map2.size(), result2.size());
            assertEquals(map3.size(), result2.size());
            assertEquals(map1.keySet(), result2.keySet());
            assertEquals(map2.keySet(), result2.keySet());
            assertEquals(map3.keySet(), result2.keySet());

            assertEquals(map1.size(), result3.size());
            assertEquals(map2.size(), result3.size());
            assertEquals(map3.size(), result3.size());
            assertEquals(map4.size(), result3.size());
            assertEquals(map1.keySet(), result3.keySet());
            assertEquals(map2.keySet(), result3.keySet());
            assertEquals(map3.keySet(), result3.keySet());
            assertEquals(map4.keySet(), result3.keySet());
        }

        /**
         * {@link Util#combineMap(Map, Map, BiFunction)} should not fail when other map has missing keys.
         */
        @Example
        void noExceptionOnMissingKey() {
            var map1 = Map.of(1, "a", 2, "b");
            var map2 = Map.of(1, "a");
            var map3 = Map.of(1, "a", 3, "c");
            var map4 = Map.of(1, "a", 3, "c", 4, "d");

            assertDoesNotThrow(() -> Util.combineMap(map1, map2, (x, y) -> x + y));
            assertDoesNotThrow(() -> Util.combineMap(map1, map2, map3, (x, y, z) -> x + y + z));
            assertDoesNotThrow(() -> Util.combineMap(map1, map2, map3, map4, (x, y, z, w) -> x + y + z + w));
        }
    }
}