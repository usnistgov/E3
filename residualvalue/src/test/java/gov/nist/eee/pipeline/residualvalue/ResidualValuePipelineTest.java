package gov.nist.eee.pipeline.residualvalue;

import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.*;
import gov.nist.eee.pipeline.DependencyParameters;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.pipeline.value.ValuePipeline;
import gov.nist.eee.tuple.Tuple2;
import net.jqwik.api.*;
import net.jqwik.api.constraints.Positive;
import net.jqwik.api.lifecycle.BeforeProperty;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.StreamSink;
import supplier.GreaterThanSupplier;
import supplier.LessThanOrEqualSupplier;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ResidualValuePipelineTest {
    static Input input;
    @Group
    class CompleteTest {
        static QuantityPipeline quantityPipeline;
        static ValuePipeline pipeline;
        static Input input;
        static StreamSink<Input> inputStream;
        static Cell<Model> cModel;
        static Cell<CellSink<Integer>> cStudyPeriod;
        @BeforeProperty
        void setup() {
            inputStream = new StreamSink<>();

            quantityPipeline = new QuantityPipeline();
            pipeline = new ValuePipeline();

            quantityPipeline.setup(inputStream, );
            var quantityOutput = quantityPipeline.define();
            cModel = quantityPipeline.getAssignableInputs();
            pipeline.setup(inputStream, );

            cStudyPeriod = cModel.map(c -> c.intInputs().get(new String[]{"analysisObject", "studyPeriod"}));
            var parameters = new DependencyParameters();
            parameters.add(QuantityPipeline.class, quantityOutput);
            pipeline.setupDependency(parameters);

            pipeline.setupInput(cModel);

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
                    )
            );
        }

        @Example
        @Disabled
        void test() {

        }
    }

    @Group
    class EndDateWithinPeriod {
        /**
         * {@link ResidualValuePipeline#endDateWithinPeriod(int, int)} should return true when the end point is larger
         * than or equal to the study period.
         */
        @Property
        void TrueWhenEndIsLessThanOrEqualStudyPeriod(
                @ForAll(supplier = LessThanOrEqualSupplier.class) Tuple2<Integer, Integer> values
        ) {
            var larger = values.e1();
            var smaller = values.e2();

            assertTrue(ResidualValuePipeline.endDateWithinPeriod(larger, smaller));
        }

        /**
         * {@link ResidualValuePipeline#endDateWithinPeriod(int, int)} should return false when the end point is less
         * than the study period.
         */
        @Property
        void FalseWhenEndIsGreaterThanStudyPeriod(
                @ForAll(supplier = GreaterThanSupplier.class) Tuple2<Integer, Integer> values
        ) {
            var larger = values.e1();
            var smaller = values.e2();

            assertFalse(ResidualValuePipeline.endDateWithinPeriod(smaller, larger));
        }
    }

    @Group
    class LastInterval {
        @Property
        void equalsStudyPeriodWhenIntervalIsOne(@ForAll @Positive int studyPeriod) {
            var result = ResidualValuePipeline.lastInterval(studyPeriod, 0, 1);
            assertEquals(studyPeriod, result);
        }

        @Property
        void zeroIntervalReturnsInitial(@ForAll @Positive int studyPeriod, @ForAll @Positive int initial) {
            var result = ResidualValuePipeline.lastInterval(studyPeriod, initial, 0);
            assertEquals(initial, result);
        }

        @Data
        Iterable<Tuple.Tuple4<Integer, Integer, Integer, Integer>> cases() {
            return Table.of(
                    // Study period, initial, interval
                    Tuple.of(25, 10, 2, 24),
                    Tuple.of(25, 0, 2, 24),
                    Tuple.of(25, 5, 2, 25),
                    Tuple.of(25, 23, 2, 25),
                    Tuple.of(50, 0, 1, 50),
                    Tuple.of(25, 0, 7, 21),
                    Tuple.of(25, 2, 7, 23),
                    Tuple.of(25, 1, 0, 1)
            );
        }

        @Property
        @FromData("cases")
        void casesTest(@ForAll int studyPeriod, @ForAll int initial, @ForAll int interval, @ForAll int result) {
            assertEquals(result, ResidualValuePipeline.lastInterval(studyPeriod, initial, interval));
        }
    }

    @Group
    class LifetimeWithinPeriod {
        @Data
        Iterable<Tuple.Tuple5<Integer, Integer, Integer, Integer, Boolean>> cases() {
            return Table.of(
                    // Study Period, Life, Initial, Interval, Result
                    Tuple.of(25, 0, 1, 0, true),
                    Tuple.of(25, 10, 24, 0, false),
                    Tuple.of(11, 2, 6, 0, true),
                    Tuple.of(11, 2, 4, 6, true)
            );
        }

        @Property
        @FromData("cases")
        void casesTest(
                @ForAll int studyPeriod,
                @ForAll int life,
                @ForAll int initial,
                @ForAll int interval,
                @ForAll boolean result
        ) {
            assertEquals(result, ResidualValuePipeline.lifetimeWithinPeriod(studyPeriod, life, initial, interval));
        }
    }

    @Group
    class RemainingLifeNonRecurring {
        @Data
        Iterable<Tuple.Tuple4<Integer, Integer, Integer, Double>> cases() {
            return Table.of(
                    Tuple.of(25, 50, 0, 25.0),
                    Tuple.of(4, 5, 0, 1.0),
                    Tuple.of(50, 100, 25, 74.0),
                    Tuple.of(25, 50, 1, 25.0)
            );
        }

        @Property
        @FromData("cases")
        void testCases(
                @ForAll int studyPeriod, @ForAll int life, @ForAll int initial, @ForAll double result
        ) {
            assertEquals(result, ResidualValuePipeline.remainingLifeNonRecurring(studyPeriod, life, initial));
        }
    }

    @Group
    class RemainingLifeRecurring {
        @Data
        Iterable<Tuple.Tuple6<Integer, Integer, Integer, Integer, Integer, Double>> cases() {
            return Table.of(
                    // Study period, end, life, initial, interval, result
                    Tuple.of(25, 10, 2, 1, 2, 0.0),
                    Tuple.of(50, 50, 0, 0, 1, 0.0),
                    Tuple.of(25, 50, 10, 0, 7, 6.0)
                    //TODO: add more test cases
            );
        }

        @Property
        @FromData("cases")
        void testCases(
                @ForAll int studyPeriod,
                @ForAll int end,
                @ForAll int life,
                @ForAll int initial,
                @ForAll int interval,
                @ForAll double result
        ) {
            assertEquals(
                    result,
                    ResidualValuePipeline.remainingLifeRecurring(studyPeriod, end, life, initial, interval)
            );
        }
    }

    @Group
    class GetRemainingLife {

    }

    @Group
    class CalculateResidualValue {
        @Data
        Iterable<Tuple.Tuple5<Double, Integer, Integer, List<Double>, Double>> cases() {
            return Table.of(
                    // remaining, life, initial, values, result
                    Tuple.of(5.0, 10, 1, List.of(0.0, 156.0), -78.0),
                    Tuple.of(10.0, 0, 1, List.of(0.0, 100.0), Double.NEGATIVE_INFINITY)
                    //TODO: more cases
            );
        }

        @Property
        @FromData("cases")
        void testCases(
                @ForAll double remaining,
                @ForAll int life,
                @ForAll int initial,
                @ForAll List<Double> values,
                @ForAll double result
        ) {
            assertEquals(result, ResidualValuePipeline.calculateResidualValue(remaining, life, initial, values));
        }
    }
}