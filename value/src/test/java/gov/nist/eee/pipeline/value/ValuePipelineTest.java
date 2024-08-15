package gov.nist.eee.pipeline.value;

import clone.Clone;
import gov.nist.eee.error.E3Exception;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.*;
import gov.nist.eee.pipeline.DependencyParameters;
import gov.nist.eee.pipeline.quantity.QuantityPipeline;
import gov.nist.eee.util.Result;
import net.jqwik.api.*;
import net.jqwik.api.constraints.*;
import net.jqwik.api.lifecycle.BeforeProperty;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.StreamSink;
import supplier.CellSupplier;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class ValuePipelineTest {
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
            var output = pipeline.define();
            inputStream.send(input);

            System.out.println(output.sample());

            if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                System.out.println(success.value().get(0).sample());
            }
        }

        /**
         * The size of the {@link ValuePipeline}'s output should change when a new study period is sent to the model.
         */
        @Property
        void sizeChangesWithStudyPeriod(@ForAll @IntRange(max = 50) int size) {
            var output = pipeline.define();
            inputStream.send(input);

            // Send new study period
            cStudyPeriod.sample().send(size);

            // Check it actually returns result
            var result = output.sample();
            assertInstanceOf(Result.Success.class, result);

            // Check size and values
            if (result instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                var values = success.value().get(0).sample();

                assertEquals(size + 1, values.size());

                assertEquals(5.0, values.get(0));
                for (var i = 1; i < values.size(); i++) {
                    assertEquals(0.0, values.get(i));
                }
            }
        }

        @Example
        void withRecurVarValue() {
            var newBcn = Clone.clone(input.bcnObjects().get(0), Map.of(
                    "recur",
                    new RecurOptions(2, VarRate.PERCENT_DELTA, List.of(1.0), 10))
            );
            var newInput = Clone.clone(input, Map.of("bcnObjects", List.of(newBcn)));

            var output = pipeline.define();
            inputStream.send(newInput);

            System.out.println(output.sample());

            if (output.sample() instanceof Result.Success<Map<Integer, Cell<List<Double>>>, E3Exception> success) {
                System.out.println(success.value().get(0).sample());
            }
        }
    }

    @Group
    class ShouldUseVarRateMap {
        /**
         * {@link ValuePipeline#shouldUseVarRateMap(List, VarRate)} should return true when both parameters are
         * non-null.
         */
        @Property
        void trueWhenBothParametersNonNull(@ForAll List<Double> varValues, @ForAll VarRate varRate) {
            var result = ValuePipeline.shouldUseVarRateMap(varValues, varRate);
            assertTrue(result);
        }

        /**
         * {@link ValuePipeline#shouldUseVarRateMap(List, VarRate)} should return false when just the var value
         * parameter is null.
         */
        @Property
        void falseWhenVarValueIsNull(@ForAll VarRate varRate) {
            var result = ValuePipeline.shouldUseVarRateMap(null, varRate);
            assertFalse(result);
        }

        /**
         * {@link ValuePipeline#shouldUseVarRateMap(List, VarRate)} should return null when just the var rate
         * parameter is null.
         */
        @Property
        void falseWhenVarRateIsNull(@ForAll List<Double> varValues) {
            var result = ValuePipeline.shouldUseVarRateMap(varValues, null);
            assertFalse(result);
        }

        /**
         * {@link ValuePipeline#shouldUseVarRateMap(List, VarRate)} should return false when both parameters are null.
         */
        @Example
        void falseWhenBothParametersAreNull() {
            var result = ValuePipeline.shouldUseVarRateMap(null, null);
            assertFalse(result);
        }
    }

    @Group
    class CalculateValues {
        @Property
        void returnMultiplyByValueWhenVarValueIsNull(
                @ForAll(supplier = CellSupplier.class) Cell<List<Double>> cQuantities,
                @ForAll(supplier = CellSupplier.class) Cell<Double> cValuePerQ,
                @ForAll VarRate varRate
        ) {
            var size = cQuantities.sample().size();
            var result = ValuePipeline.calculateValues(cQuantities, cValuePerQ, null, varRate, size);

            assertInstanceOf(Result.Success.class, result);
            if (result instanceof Result.Success<Cell<List<Double>>, E3Exception> success)
                assertEquals(ValuePipeline.multiplyByValue(cQuantities, cValuePerQ).sample(), success.value().sample());
        }

        @Property
        void returnMultiplyByValueWhenVarRateIsNull(
                @ForAll(supplier = CellSupplier.class) Cell<List<Double>> cQuantities,
                @ForAll(supplier = CellSupplier.class) Cell<Double> cValuePerQ,
                @ForAll List<Double> varValue
        ) {
            var size = cQuantities.sample().size();
            var result = ValuePipeline.calculateValues(cQuantities, cValuePerQ, varValue, null, size);

            assertInstanceOf(Result.Success.class, result);
            if (result instanceof Result.Success<Cell<List<Double>>, E3Exception> success)
                assertEquals(ValuePipeline.multiplyByValue(cQuantities, cValuePerQ).sample(), success.value().sample());
        }

        @Property
        void returnMultiplyByValueWhenBothVarValueAndVarRateAreNull(
                @ForAll(supplier = CellSupplier.class) Cell<List<Double>> cQuantities,
                @ForAll(supplier = CellSupplier.class) Cell<Double> cValuePerQ
        ) {
            var size = cQuantities.sample().size();
            var result = ValuePipeline.calculateValues(cQuantities, cValuePerQ, null, null, size);

            assertInstanceOf(Result.Success.class, result);
            if (result instanceof Result.Success<Cell<List<Double>>, E3Exception> success)
                assertEquals(ValuePipeline.multiplyByValue(cQuantities, cValuePerQ).sample(), success.value().sample());
        }

        //TODO
    }

    @Group
    class GetUsingVarRateMap {
        /**
         * {@link ValuePipeline#getUsingVarRateMap(Cell, Cell, List, VarRate, int)} should return a list whose size is
         * equal to the study period + 1 with a var value of one element and any other valid inputs.
         */
        @Property
        void varValueOfSizeOneReturnsListWithCorrectSize(
                @ForAll(supplier = CellSupplier.class) Cell<@Size(min = 1, max = 50) List<Double>> cQuantities,
                @ForAll(supplier = CellSupplier.class) Cell<Double> cValuePerQ,
                @ForAll VarRate varRate
        ) {
            var size = cQuantities.sample().size();
            var studyPeriod = size - 1;
            var result = ValuePipeline.getUsingVarRateMap(cQuantities, cValuePerQ, List.of(1.0), varRate, studyPeriod);

            assertInstanceOf(Result.Success.class, result);
            if (result instanceof Result.Success<Cell<List<Double>>, E3Exception> success) {
                var list = success.value().sample();
                assertEquals(studyPeriod + 1, list.size());
            }

            System.out.println();
            //    assertEquals(ValuePipeline.multiplyByValue(cQuantities, cValuePerQ).sample(), success.value().sample());
        }

        /**
         * {@link ValuePipeline#getUsingVarRateMap(Cell, Cell, List, VarRate, int)} should return a list whose size is
         * equal to the study period + 1 with a var value of study period + 1 elements and any other valid inputs.
         */
        @Property
        void varValueOfStudyPeriodSizeReturnsListWithCorrectSize(
                @ForAll(supplier = CellSupplier.class) Cell<@Size(min = 1, max = 50) List<Double>> cQuantities,
                @ForAll(supplier = CellSupplier.class) Cell<Double> cValuePerQ,
                @ForAll VarRate varRate
        ) {
            var size = cQuantities.sample().size();
            var studyPeriod = size - 1;

            var varValue = new ArrayList<Double>(size);
            for (var i = 0; i < size; i++) {
                varValue.add(1.0);
            }

            var result = ValuePipeline.getUsingVarRateMap(cQuantities, cValuePerQ, varValue, varRate, studyPeriod);

            assertInstanceOf(Result.Success.class, result);
            if (result instanceof Result.Success<Cell<List<Double>>, E3Exception> success) {
                var list = success.value().sample();
                assertEquals(studyPeriod + 1, list.size());
            }
        }
    }
}