package gov.nist.eee.pipeline.quantity;

import clone.Clone;
import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.input.*;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.Util;
import net.jqwik.api.*;
import net.jqwik.api.constraints.*;
import net.jqwik.api.lifecycle.BeforeProperty;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.StreamSink;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import supplier.CellSinkSupplier;
import supplier.CellSupplier;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mockStatic;

class QuantityPipelineTest {


    @Group
    class CompleteTest {
        static QuantityPipeline pipeline;
        static Input input;

        @BeforeProperty
        void setup() {
            pipeline = new QuantityPipeline();

            input = new Input(
                    new Analysis(
                            null,
                            null,
                            List.of("quantity"),
                            25,
                            TimestepValue.YEAR,
                            TimestepComp.END_OF_YEAR,
                            true,
                            0.06,
                            0.06,
                            0.06,
                            0.06,
                            0.06,
                            0.06,
                            0.06,
                            0.06,
                            null,
                            0
                    ),
                    List.of(
                            new Bcn(
                                    0,
                                    List.of(0),
                                    BcnType.COST,
                                    BcnSubType.DIRECT,
                                    "Bcn 1",
                                    null,
                                    0,
                                    true,
                                    false,
                                    5,
                                    false,
                                    false,
                                    null,
                                    0.05,
                                    100,
                                    null,
                                    null,
                                    null
                            )
                    ),
                    Map.of()
            );
        }

        @Test
        void testRecurring() {
            input = new Input(
                    new Analysis(
                            AnalysisType.BCA,
                            ProjectType.INFRASTRUCTURE,
                            List.of("quantity"),
                            50,
                            TimestepValue.YEAR,
                            TimestepComp.END_OF_YEAR,
                            true,
                            null,
                            0.03,
                            null,
                            0.023,
                            0.03,
                            0.03,
                            null,
                            null,
                            null,
                            0
                    ),
                    List.of(
                            new Bcn(
                                    0,
                                    List.of(0),
                                    BcnType.COST,
                                    BcnSubType.DIRECT,
                                    "Investment Cost - Status Quo",
                                    List.of("Initial Investment"),
                                    0,
                                    true,
                                    true,
                                    null,
                                    false,
                                    false,
                                    null,
                                    0.0,
                                    1,
                                    null,
                                    null,
                                    null
                            ),
                            new Bcn(
                                    1,
                                    List.of(1),
                                    BcnType.COST,
                                    BcnSubType.DIRECT,
                                    "Construct Monument",
                                    List.of("Investment Cost"),
                                    0,
                                    true,
                                    true,
                                    null,
                                    false,
                                    false,
                                    null,
                                    100000.0,
                                    1,
                                    null,
                                    null,
                                    null
                            ),
                            new Bcn(
                                    2,
                                    List.of(1),
                                    BcnType.COST,
                                    BcnSubType.DIRECT,
                                    "Maintain Monument",
                                    List.of("OMR Costs"),
                                    1,
                                    true,
                                    false,
                                    50,
                                    false,
                                    false,
                                    new RecurOptions(
                                            1,
                                            VarRate.PERCENT_DELTA,
                                            List.of(0.0),
                                            0
                                    ),
                                    100000.0,
                                    1,
                                    null,
                                    null,
                                    null
                            )
                    ),
                    Map.of()
            );

            var stream = new StreamSink<Input>();

            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(input);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                System.out.println(success.value());
            }
        }

        /**
         * {@link QuantityPipeline}'s define method should not return null.
         */
        @Example
        void defineReturnsNonNull() {
            var stream = new StreamSink<Input>();

            pipeline.setup(stream);
            var result = pipeline.define();

            stream.send(input);

            assertNotNull(result);
        }

        /**
         * {@link QuantityPipeline} should output non-null lists.
         */
        @Example
        void outputIsNonNullList() {
            var stream = new StreamSink<Input>();

            pipeline.setup(stream);
            var output = pipeline.define();

            stream.send(input);
            var res = output.sample();

            if (res instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();

                assertNotNull(result);
                assertInstanceOf(List.class, result);
            } else if (res instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>) {
                fail();
            }
        }

        /**
         * {@link QuantityPipeline} should output a failure when the quantity var value is not of size one or the
         * same size as the study period + 1.
         */
        @Example
        void failsWhenVarValueIsNotCorrectSize() {
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of(
                    "quantityVarValue", List.of(1.0, 2.0, 3.0),
                    "quantityVarRate", VarRate.PERCENT_DELTA
            ));
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            var res = output.sample();

            if (res instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception>) {
                fail("Should not succeed");
            } else if (res instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception> failure) {
                assertEquals(failure.error().code(), ErrorCode.E7104_PARTIALLY_DEFINED_VAR_VALUE);
            }
        }

        /**
         * {@link QuantityPipeline} should output lists with the correct length of study period + 1. Limited to study
         * period {@code 1 <= studyPeriod <= 500} to prevent out of memory exceptions.
         */
        @Property
        void outputIsCorrectSize(@ForAll @IntRange(min = 1, max = 500) int studyPeriod) {
            // Setup input
            var newAnalysis = Clone.clone(input.analysis(), Map.of("studyPeriod", studyPeriod));
            var newInput = Clone.clone(input, Map.of("analysis", newAnalysis));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();

                assertEquals(studyPeriod + 1, result.size());
            }
        }

        @Example
        void everyOtherInterval() {
            // Setup input
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of("recur", new RecurOptions(2, null, null, 10)));
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();
                var expected = List.of(100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);

                assertEquals(expected, result);
            }
        }

        @Example
        void everyThreeInterval() {
            // Setup input
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of("recur", new RecurOptions(3, null, null, 10)));
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();
                var expected = List.of(100.0, 0.0, 0.0, 100.0, 0.0, 0.0, 100.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);

                assertEquals(expected, result);
            }
        }

        /**
         * {@link QuantityPipeline} should put the first quantity occurrence on the same timestep as the
         * initialOccurrence parameter.
         */
        @Property
        void differentInitialOccurrences(@ForAll @IntRange(max = 25) int initial) {
            // Setup input
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of("initialOccurrence", initial));
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();

                for (int i = 0; i < result.size(); i++) {
                    if (i == initial)
                        assertEquals(100.0, result.get(i));
                    else
                        assertEquals(0.0, result.get(i));
                }
            }
        }

        /**
         * {@link QuantityPipeline} should not place quantity values after the given end date for the BCN.
         */
        @Property
        void end(@ForAll @IntRange(max = 25) int end) {
            // Setup input
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of("recur", new RecurOptions(1, null, null, end)));
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();

                for (int i = 0; i < result.size(); i++) {
                    if (i <= end)
                        assertEquals(100.0, result.get(i));
                    else
                        assertEquals(0.0, result.get(i));

                }
            }
        }

        /**
         * {@link QuantityPipeline} interval works even when initial occurrence is not default.
         */
        @Example
        void initialOccurrenceWithInterval() {
            // Setup input
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of("initialOccurrence", 2, "recur", new RecurOptions(3, null, null, 10)));
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();
                var expected = List.of(0.0, 0.0, 100.0, 0.0, 0.0, 100.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);

                assertEquals(expected, result);
            }
        }

        /**
         * {@link QuantityPipeline} should accept a single var value and assume it should be used for all values in the
         * cashflow.
         */
        @Example
        void singleVarValue() {
            // Setup input
            var newBcn = Clone.clone(
                    input.bcnObjects().get(0),
                    Map.of(
                            "quantityVarRate", VarRate.PERCENT_DELTA,
                            "quantityVarValue", List.of(1.0),
                            "recur", new RecurOptions(1, null, null, 10)
                    )
            );
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();

                assertEquals(
                        List.of(100.0, 200.0, 400.0, 800.0, 1600.0, 3200.0, 6400.0, 12800.0, 25600.0, 51200.0, 102400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                        result
                );
            }
        }

        /**
         * {@link QuantityPipeline} should accept a list of var values and apply them to the cashflow.
         */
        @Example
        void multipleVarValue() {
            // Setup input
            var newBcn = Clone.clone(
                    input.bcnObjects().get(0),
                    Map.of(
                            "quantityVarRate", VarRate.PERCENT_DELTA,
                            "quantityVarValue", List.of(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                            "recur", new RecurOptions(1, null, null, 10)
                    )
            );
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));
            var stream = new StreamSink<Input>();

            // Setup pipeline and send input
            pipeline.setup(stream);
            var output = pipeline.define();
            stream.send(newInput);

            // Check result
            if (output.sample() instanceof Result.Failure<Map<Integer, Cell<List<Double>>>, E3Exception>)
                fail();
            else if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var result = success.value().get(0).sample();

                assertEquals(
                        List.of(100.0, 200.0, 400.0, 800.0, 1600.0, 3200.0, 6400.0, 12800.0, 25600.0, 51200.0, 102400.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                        result
                );
            }
        }
    }

    @Group
    class IsOutside {
        /**
         * {@link QuantityPipeline#isOutside(int, int, int, int)} should return false whenever the {@code initial}
         * parameter is negative. This hold for any values of the other three parameters.
         */
        @Property
        void firstParamNegative(@ForAll @Negative int a, @ForAll int b, @ForAll int c, @ForAll int d) {
            assertFalse(QuantityPipeline.isOutside(a, b, c, d));
        }

        /**
         * {@link QuantityPipeline#isOutside(int, int, int, int)} should start returning false when the {@code index}
         * parameter is equal to the {@code initial} parameter. This should hold for any interval and any end point
         * as long as end is greater than initial.
         */
        @Example
        void startsAtInitial(@ForAll @IntRange int interval, @ForAll @IntRange(min = 2) int end) {
            assertTrue(QuantityPipeline.isOutside(0, 1, interval, end));
            assertFalse(QuantityPipeline.isOutside(1, 1, interval, end));

            assertTrue(QuantityPipeline.isOutside(0, 2, interval, end));
            assertTrue(QuantityPipeline.isOutside(1, 2, interval, end));
            assertFalse(QuantityPipeline.isOutside(2, 2, interval, end));
        }

        /**
         * {@link QuantityPipeline#isOutside(int, int, int, int)} should return true when the index is strictly greater
         * than the {@code end} parameter. This should hold for any {@code interval} size.
         */
        @Example
        void stopsAtEnd(@ForAll @IntRange int interval) {
            // With any interval
            assertTrue(QuantityPipeline.isOutside(4, 1, interval, 3));
            assertTrue(QuantityPipeline.isOutside(5, 1, interval, 3));

            // With explicit index which is inside
            assertFalse(QuantityPipeline.isOutside(2, 1, 1, 4));
            assertFalse(QuantityPipeline.isOutside(3, 1, 1, 4));
            assertFalse(QuantityPipeline.isOutside(4, 1, 1, 4));
            assertTrue(QuantityPipeline.isOutside(5, 1, 1, 4));
            assertTrue(QuantityPipeline.isOutside(6, 1, 1, 4));
        }

        /**
         * {@link QuantityPipeline#isOutside(int, int, int, int)} should return true only on the intervals specified.
         */
        @Example
        void interval() {
            // Every other interval
            assertTrue(QuantityPipeline.isOutside(0, 1, 2, 5));
            assertFalse(QuantityPipeline.isOutside(1, 1, 2, 5));
            assertTrue(QuantityPipeline.isOutside(2, 1, 2, 5));
            assertFalse(QuantityPipeline.isOutside(3, 1, 2, 5));
            assertTrue(QuantityPipeline.isOutside(4, 1, 2, 5));
            assertFalse(QuantityPipeline.isOutside(5, 1, 2, 5));
            assertTrue(QuantityPipeline.isOutside(6, 1, 2, 5));

            // Every three
            assertTrue(QuantityPipeline.isOutside(0, 1, 3, 5));
            assertFalse(QuantityPipeline.isOutside(1, 1, 3, 5));
            assertTrue(QuantityPipeline.isOutside(2, 1, 3, 5));
            assertTrue(QuantityPipeline.isOutside(3, 1, 3, 5));
            assertFalse(QuantityPipeline.isOutside(4, 1, 3, 5));
            assertTrue(QuantityPipeline.isOutside(5, 1, 3, 5));
            assertTrue(QuantityPipeline.isOutside(6, 1, 3, 5));

            // Every four
            assertTrue(QuantityPipeline.isOutside(0, 1, 4, 5));
            assertFalse(QuantityPipeline.isOutside(1, 1, 4, 5));
            assertTrue(QuantityPipeline.isOutside(2, 1, 4, 5));
            assertTrue(QuantityPipeline.isOutside(3, 1, 4, 5));
            assertTrue(QuantityPipeline.isOutside(4, 1, 4, 5));
            assertFalse(QuantityPipeline.isOutside(5, 1, 4, 5));
            assertTrue(QuantityPipeline.isOutside(6, 1, 4, 5));

            // ...etc
        }
    }

    @Group
    class GetEndPoint {
        @Property
        void recurringFalseReturnsInitial(
                @ForAll(supplier = CellSinkSupplier.class) CellSink<Integer> end,
                @ForAll(supplier = CellSinkSupplier.class) CellSink<Integer> initial,
                @ForAll(supplier = CellSupplier.class) Cell<CellSink<Integer>> studyPeriod
        ) {
            var result = QuantityPipeline.getEndPoint(false, end, initial, studyPeriod);
            assertEquals(initial, result);
        }

        @Property
        void recurringTrueReturnsEnd(
                @ForAll(supplier = CellSinkSupplier.class) CellSink<Integer> end,
                @ForAll(supplier = CellSinkSupplier.class) CellSink<Integer> initial,
                @ForAll(supplier = CellSupplier.class) Cell<CellSink<Integer>> studyPeriod
        ) {
            var result = QuantityPipeline.getEndPoint(true, end, initial, studyPeriod);
            assertEquals(end, result);
        }

        @Property
        void nullEndReturnsStudyPeriod(
                @ForAll(supplier = CellSinkSupplier.class) CellSink<Integer> initial,
                @ForAll(supplier = CellSupplier.class) Cell<CellSink<Integer>> studyPeriod
        ) {
            var result = QuantityPipeline.getEndPoint(true, null, initial, studyPeriod);
            assertEquals(studyPeriod.sample().sample(), result.sample());
        }
    }


    @Group
    class IsBeforeInitial {
        /**
         * {@link QuantityPipeline#isBeforeInitial(int, int)} should returns false whenever the first parameter is
         * negative.
         */
        @Property
        void negativeFirstParam(@ForAll @Negative int a, @ForAll int b) {
            assertFalse(QuantityPipeline.isBeforeInitial(a, b));
        }

        /**
         * {@link QuantityPipeline#isBeforeInitial(int, int)} should return false whenever the second parameter is
         * negative.
         */
        @Property
        void negativeSecondParam(@ForAll @Negative int a, @ForAll int b) {
            assertFalse(QuantityPipeline.isBeforeInitial(a, b));
        }

        /**
         * {@link QuantityPipeline#isBeforeInitial(int, int)} when both parameter are greater than or equal to 0, it
         * should return the result of {@code a < b} where {@code a} is the first parameter and {@code b} is the second
         * parameter.
         */
        @Property
        void positive(@ForAll @IntRange int a, @ForAll @IntRange int b) {
            assertEquals(a < b, QuantityPipeline.isBeforeInitial(a, b));
        }
    }

    @Group
    class IsNotInIntervalGroup {

        /**
         * {@link QuantityPipeline#isNotInInterval(int, int, int)} should return false whenever the first parameter is
         * negative.
         */
        @Property
        void returnsFalseForNegativeFirstParam(@ForAll @Negative int a, @ForAll int b, @ForAll int c) {
            assertFalse(QuantityPipeline.isNotInInterval(a, b, c));
        }

        /**
         * {@link QuantityPipeline#isNotInInterval(int, int, int)} should return false whenever the second parameter is
         * negative.
         */
        @Property
        void returnsFalseForNegativeSecondParam(@ForAll int a, @ForAll @Negative int b, @ForAll int c) {
            assertFalse(QuantityPipeline.isNotInInterval(a, b, c));
        }

        /**
         * {@link QuantityPipeline#isNotInInterval(int, int, int)} should return false whenever the third parameter is
         * negative.
         */
        @Property
        void returnsFalseForNegativeThirdParam(@ForAll int a, @ForAll int b, @ForAll @Negative int c) {
            assertFalse(QuantityPipeline.isNotInInterval(a, b, c));
        }

        /**
         * {@link QuantityPipeline#isNotInInterval(int, int, int)} should return false when the {@code interval}
         * parameter is 0 regardless of the values of the other two parameters.
         */
        @Property
        void returnsFalseWhenZero(@ForAll int a, @ForAll int b) {
            assertFalse(QuantityPipeline.isNotInInterval(a, b, 0));
        }

        /**
         * {@link QuantityPipeline#isNotInInterval(int, int, int)} should return true when the modulus of the
         * {@code index} and the {@code interval} parameter equals 0 given the {@index initial} parameter is 0.
         */
        @Property
        void returnsModulo(@ForAll @Positive int a, @ForAll @Positive int b) {
            assertEquals(a % b != 0, QuantityPipeline.isNotInInterval(a, 0, b));
        }

        /**
         * {@link QuantityPipeline#isNotInInterval(int, int, int)} should return true when the modulus of the
         * {@code index} minus the {@code initial} parameter and the {@code interval} parameter equals 0.
         */
        @Property
        void returnsModuloMinusStart(@ForAll @Positive int a, @ForAll @Positive int b, @ForAll @Positive int c) {
            assertEquals((a - b) % c != 0, QuantityPipeline.isNotInInterval(a, b, c));
        }
    }

    @Group
    class IsAfterEnd {
        /**
         * {@link QuantityPipeline#isAfterEnd(int, int)} should return false whenever the first parameter is negative.
         */
        @Property
        void isAfterEndFalseForFirstParam(@ForAll @Negative int a, @ForAll int b) {
            assertFalse(QuantityPipeline.isAfterEnd(a, b));
        }

        /**
         * {@link QuantityPipeline#isAfterEnd(int, int)} should return false whenever the second parameter is negative.
         */
        @Property
        void isAfterEndFalseForSecondParam(@ForAll int a, @ForAll @Negative int b) {
            assertFalse(QuantityPipeline.isAfterEnd(a, b));
        }

        /**
         * {@link QuantityPipeline#isAfterEnd(int, int)} should return whether the first parameter is greater than the
         * second parameter given both parameters are greater than or equal to 0.
         */
        @Property
        void isAfterEndReturnsGreaterThan(@ForAll @IntRange int a, @ForAll @IntRange int b) {
            assertEquals(a > b, QuantityPipeline.isAfterEnd(a, b));
        }
    }

    @Group
    class MapWithVarRate {
        /**
         * {@link QuantityPipeline#mapWithVarRate(List, VarRate)} should return an empty list when either of the two
         * parameters are null.
         */
        @Property
        void nullValuesReturnsEmptyList(@ForAll List<Double> values, @ForAll VarRate varRate) {
            assertEquals(List.of(), QuantityPipeline.mapWithVarRate(null, varRate));
            assertEquals(List.of(), QuantityPipeline.mapWithVarRate(values, null));
        }

        /**
         * {@link QuantityPipeline#mapWithVarRate(List, VarRate)} should return the same input list when the var rate
         * parameter is {@link VarRate#YEAR_BY_YEAR}.
         */
        @Property
        void yearByYearReturnsSameValues(@ForAll List<Double> values) {
            assertEquals(values, QuantityPipeline.mapWithVarRate(values, VarRate.YEAR_BY_YEAR));
        }

        /**
         * {@link QuantityPipeline#mapWithVarRate(List, VarRate, Function)} should call the function passed in as a
         * parameter when the var rate parameter is set to {@link VarRate#PERCENT_DELTA}.
         */
        @Property
        void percentDeltaCallsCompound(@ForAll List<Double> values) {
            final var TEST_LIST = List.of(1.0, 5.5, 10.1);

            try (var mockUtil = mockStatic(Util.class)) {
                // Set up return type for static mock function
                mockUtil.when(() -> Util.compound(Mockito.anyList())).thenReturn(TEST_LIST);

                // Run method
                var result = QuantityPipeline.mapWithVarRate(values, VarRate.PERCENT_DELTA, Util::compound);

                // Test result and that function was called
                assertEquals(TEST_LIST.size(), result.size());
                mockUtil.verify(() -> Util.compound(values));
            }
        }

        /**
         * {@link QuantityPipeline#mapWithVarRate(List, VarRate)} should default to calling {@link Util#compound(List)}
         * when no other function parameter is given.
         */
        @Property
        void defaultPercentDeltaUsesUtilCompound(@ForAll List<Double> values) {
            var result = QuantityPipeline.mapWithVarRate(values, VarRate.PERCENT_DELTA);
            assertEquals(Util.compound(values), result);
        }
    }

    @Group
    class ReplaceOutside {
        /**
         * {@link QuantityPipeline#replaceOutside(List, int, int, int)} should return a list that is the same size as
         * the input.
         */
        @Property
        void resultIsSameSize(@ForAll List<Double> values, @ForAll int initial, @ForAll int interval, @ForAll int end) {
            assertEquals(values.size(), QuantityPipeline.replaceOutside(values, initial, interval, end).size());
        }

        /**
         * {@link QuantityPipeline#replaceOutside(List, int, int, int)} should return a list with indicies replaced with
         * 0.0 when {@link QuantityPipeline#isOutside(int, int, int, int)} returns true.
         */
        @Property
        void replacesWithZeros(@ForAll List<Double> values, @ForAll int initial, @ForAll int interval, @ForAll int end) {
            var result = QuantityPipeline.replaceOutside(values, initial, interval, end);

            for (int i = 0; i < result.size(); i++) {
                if (QuantityPipeline.isOutside(i, initial, interval, end))
                    assertEquals(result.get(i), 0.0);
                else
                    assertEquals(values.get(i), result.get(i));
            }
        }
    }

    @Group
    class ShouldInflate {
        /**
         * {@link QuantityPipeline#shouldInflate(Map, Map)} should return a map that is the same size as the input and
         * has the same keys.
         */
        @Property
        void sameSizeAndKeys(@ForAll("shouldInflateInput") Tuple.Tuple2<Map<Integer, VarRate>, Map<Integer, List<Double>>> inputs) {
            var rates = inputs.get1();
            var values = inputs.get2();

            var result = QuantityPipeline.shouldInflate(rates, values);

            assertEquals(rates.size(), result.size());
            assertEquals(values.size(), result.size());

            assertEquals(rates.keySet(), result.keySet());
            assertEquals(values.keySet(), result.keySet());

            for (var bool : result.values()) {
                assertFalse(bool);
            }
        }

        /**
         * {@link QuantityPipeline#shouldInflate(Map, Map)} should return true for entries with a null {@link VarRate}.
         */
        @Example
        void falseForNullVarRate() {
            var rates = new HashMap<Integer, VarRate>();
            rates.put(1, VarRate.PERCENT_DELTA);
            rates.put(2, null);
            rates.put(3, VarRate.YEAR_BY_YEAR);

            var values = Map.of(1, List.of(1.0, 2.0), 2, List.of(3.0, 4.0), 3, List.of(5.0, 6.0));

            var result = QuantityPipeline.shouldInflate(rates, values);

            assertEquals(Map.of(1, false, 2, true, 3, false), result);
        }

        /**
         * {@link QuantityPipeline#shouldInflate(Map, Map)} should return true for entries with a null value list.
         */
        @Example
        void falseForNullValues() {
            var values = new HashMap<Integer, List<Double>>();
            values.put(1, List.of(1.0, 2.0));
            values.put(2, null);
            values.put(3, List.of(5.0, 6.0));

            var rates = Map.of(1, VarRate.PERCENT_DELTA, 2, VarRate.PERCENT_DELTA, 3, VarRate.YEAR_BY_YEAR);

            var result = QuantityPipeline.shouldInflate(rates, values);

            assertEquals(Map.of(1, false, 2, true, 3, false), result);
        }

        @Provide
        Arbitrary<Tuple.Tuple2<Map<Integer, VarRate>, Map<Integer, List<Double>>>> shouldInflateInput() {
            var doubleArbitrary = Arbitraries.doubles();

            var rateArbitrary = Arbitraries.maps(Arbitraries.integers(), Arbitraries.of(VarRate.class));

            return rateArbitrary.map(
                    map -> {
                        var result = map.entrySet()
                                .stream()
                                .collect(Collectors.toMap(Map.Entry::getKey, (entry) -> doubleArbitrary.list().sample()));

                        return Tuple.of(map, result);
                    }
            );
        }
    }

    @Group
    class InflateVarValue {
        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should throw an {@link IllegalArgumentException} when the
         * size parameter is less than or equal to zero.
         */
        @Property
        void negativeOrZeroSizeThrowsException(
                @ForAll List<Double> values,
                @ForAll @IntRange(min = Integer.MIN_VALUE, max = 0) int size
        ) {
            var result = QuantityPipeline.inflateVarValue(values, size);

            assertInstanceOf(Result.Failure.class, result);

            if (result instanceof Result.Failure<List<Double>, E3Exception> failure)
                assertEquals(ErrorCode.E7102_INFLATE_LESS_THAN_ONE, failure.error().code());
        }

        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should trow an {@link IllegalArgumentException} when the
         * values parameter is null and the size parameter is {@code >= 1}.
         */
        @Property
        void throwsExceptionWhenVarValueIsNull(@ForAll @IntRange(min = 1) int size) {
            var result = QuantityPipeline.inflateVarValue(null, size);

            assertInstanceOf(Result.Failure.class, result);

            if (result instanceof Result.Failure<List<Double>, E3Exception> failure)
                assertEquals(ErrorCode.E7103_VAR_VALUE_NULL, failure.error().code());
        }

        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should return the input values if the size is the same
         * as the value list size.
         */
        @Property
        void returnsVarValueWhenItsLengthIsTheSameAsSize(@ForAll @NotEmpty List<Double> values) {
            var result = QuantityPipeline.inflateVarValue(values, values.size());

            assertInstanceOf(Result.Success.class, result);

            if (result instanceof Result.Success<List<Double>, E3Exception> success) {
                var value = success.value();

                assertEquals(values, value);
                assertSame(values, value);
            }
        }

        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should throw an {@link IllegalArgumentException} when the
         * values array has more than one element and does not equal the size parameter.
         */
        @Property
        void valuesMustOnlyHaveOneElementIfNotEqualToSize(@ForAll @Size(min = 2) List<Double> values) {
            var result = QuantityPipeline.inflateVarValue(values, values.size() + 1);

            assertInstanceOf(Result.Failure.class, result);

            if (result instanceof Result.Failure<List<Double>, E3Exception> failure)
                assertEquals(ErrorCode.E7104_PARTIALLY_DEFINED_VAR_VALUE, failure.error().code());
        }

        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should throw an {@link IllegalArgumentException} when given
         * an empty list.
         */
        @Example
        void throwsExceptionForEmtpyList() {
            var result = QuantityPipeline.inflateVarValue(List.of(), 2);

            assertInstanceOf(Result.Failure.class, result);

            if (result instanceof Result.Failure<List<Double>, E3Exception> failure)
                assertEquals(ErrorCode.E7104_PARTIALLY_DEFINED_VAR_VALUE, failure.error().code());
        }

        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should return a list that is the same length as the input
         * size parameter for valid inputs.
         */
        @Property
        void returnsListOfSize(
                @ForAll @Size(value = 1) List<Double> values,
                @ForAll @IntRange(min = 1, max = 100) int size
        ) {
            var result = QuantityPipeline.inflateVarValue(values, size);

            assertInstanceOf(Result.Success.class, result);

            if(result instanceof Result.Success<List<Double>, E3Exception> success)
                assertEquals(size, success.value().size());
        }

        /**
         * {@link QuantityPipeline#inflateVarValue(List, int)} should return a list with the first element being zero and
         * all the subsequent elements being equal to the single element in the values list.
         */
        @Property
        void allElementsAfterFirstEqualValue(
                @ForAll @Size(value = 1) List<Double> values,
                @ForAll @IntRange(min = 2, max = 100) int size
        ) {
            var result = QuantityPipeline.inflateVarValue(values, size);

            assertInstanceOf(Result.Success.class, result);

            if(result instanceof Result.Success<List<Double>, E3Exception> success) {
                assertEquals(success.value().get(0), 0.0);

                for (int i = 1; i < values.size(); i++) {
                    assertEquals(values.get(0), success.value().get(i));
                }
            }
        }
    }

    @Group
    class VarRateMap {
    }
}