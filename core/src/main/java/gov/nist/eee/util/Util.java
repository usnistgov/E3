package gov.nist.eee.util;

import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Alternative;
import gov.nist.eee.object.tree.Tree;
import gov.nist.eee.util.Result.Failure;
import gov.nist.eee.util.Result.Success;
import gov.nist.eee.util.function.QuadFunction;
import gov.nist.eee.util.function.TriFunction;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.Lambda1;
import org.apache.commons.lang3.ClassUtils;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Parameter;
import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class Util {
    private Util() {
        throw new IllegalStateException("Cannot instantiate static utility class");
    }

    public static <K, V, A> Cell<Map<K, V>> toMap(Cell<List<A>> cValues, Function<A, K> getKey, Function<A, V> getValue) {
        return cValues.map(values -> {
            var result = new HashMap<K, V>();

            for (var value : values) {
                var key = getKey.apply(value);
                var mapValue = getValue.apply(value);

                result.put(key, mapValue);
            }

            return result;
        });
    }

    /**
     * Helper higher order function that creates a function to turn a list into a map using the given key and value
     * extractors.
     *
     * @param keyExtractor   Function that returns the map key for a value in the list.
     * @param valueExtractor Function that returns the map value for a value in the list.
     * @param <T>            The type of the list being turned into a map.
     * @param <K>            The type of the map key.
     * @param <V>            The type of the map value.
     * @return A function that accepts a list and turns it into a map.
     */
    public static <T, K, V> Lambda1<List<T>, Map<K, V>> toMap(Function<T, K> keyExtractor, Function<T, V> valueExtractor) {
        return list -> {
            var result = new HashMap<K, V>(list.size());

            for (var element : list) {
                result.put(keyExtractor.apply(element), valueExtractor.apply(element));
            }

            return result;
        };
    }

    /**
     * Helper higher order function that creates a function to turn a list into a map using the given key and value
     * extractors and then applies a mapping function to the value in the map.
     *
     * @param keyExtractor   Function that returns the map key for a value in the list.
     * @param valueExtractor Function that returns the map value for a value in the list.
     * @param mapper         Function that maps the value returned by valueExtractor into a new value of type D.
     * @param <A>            The type of the list being turned into a map.
     * @param <B>            The type of the map key.
     * @param <C>            The type of the map value before mapping.
     * @param <D>            The type of the map value after mapping.
     * @return A function that accepts a list and turns it into a map.
     */
    public static <A, B, C, D> Lambda1<List<A>, Map<B, D>> toMap(Function<A, B> keyExtractor, Function<A, C> valueExtractor, Function<C, D> mapper) {
        return toMap(keyExtractor, valueExtractor.andThen(mapper));
    }

    public static <A, B> Cell<List<B>> toList(Cell<List<A>> cValues, Function<A, B> getValue) {
        return cValues.map(values -> values.stream().map(getValue).toList());
    }

    public static <K, V, A> Cell<Map<K, CellSink<V>>> toSinkMap(Cell<List<A>> cValues, Function<A, K> getKey, Function<A, V> getValue) {
        return cValues.map(values -> values.stream().collect(Collectors.toMap(getKey, v -> new CellSink<>(getValue.apply(v)))));
    }

    public static <K, V> void addMapToTree(Map<K, V> map, Tree<String, V> tree, String path) {
        map.forEach((key, value) -> tree.add(String.format(path, key).split("[.\\[\\]]+"), value));
    }

    public static Cell<Model> createInputModel(
            Cell<Consumer<Tree<String, CellSink<Double>>>> cAddDoubleInputs,
            Cell<Consumer<Tree<String, CellSink<Integer>>>> cAddIntegerInputs
    ) {
        return cAddDoubleInputs.lift(cAddIntegerInputs, (addDoubles, addIntegers) -> {
            var doubleInputs = Tree.<String, CellSink<Double>>create();
            var integerInputs = Tree.<String, CellSink<Integer>>create();

            addDoubles.accept(doubleInputs);
            addIntegers.accept(integerInputs);

            return new Model(doubleInputs, integerInputs);
        });
    }

    /**
     * Multiplies each element in the given list by the given multiplier.
     *
     * @param values     The list of values to multiply.
     * @param multiplier The value to multiply each list value by.
     * @return A new list containing the original values multiplied by the given multiplier value.
     */
    public static List<Double> multiplier(List<Double> values, final double multiplier) {
        return values.stream().map(v -> v * multiplier).toList();
    }

    /**
     * Multiplies two lists together elementwise.
     *
     * @param left  The first list to multiply.
     * @param right The second list to multiply.
     * @return A list containing the elementwise product of the given lists.
     */
    public static List<Double> elementwiseMultiply(List<Double> left, List<Double> right) {
        return elementwise(left, right, (x, y) -> x * y);
    }

    /**
     * Performs an operation elementwise on the given lists and returns the resulting list.
     *
     * @param left      One of the lists to perform the operation on.
     * @param right     The other list to perform the operation on.
     * @param operation The operation which takes an element from the first and second list and combines them into a new
     *                  value.
     * @param <A>       The type of the first list.
     * @param <B>       The type of the second list.
     * @param <C>       The output type.
     * @return A list containing the values combined elementwise from the given arrays using the given operation.
     */
    public static <A, B, C> List<C> elementwise(List<A> left, List<B> right, BiFunction<A, B, C> operation) {
        if (left.size() != right.size())
            throw new IllegalArgumentException(
                    "An elementwise operation can only be performed on lists of the same size."
            );

        var result = new ArrayList<C>(left.size());
        for (int i = 0; i < left.size(); i++) {
            result.add(operation.apply(left.get(i), right.get(i)));
        }
        return result;
    }

    /**
     * Adds two lists together elementwise.
     *
     * @param left  The first list to add.
     * @param right The second list to add.
     * @return A list containing the elementwise sums of the given lists.
     */
    public static List<Double> elementwiseAdd(List<Double> left, List<Double> right) {
        return elementwise(left, right, Double::sum);
    }

    public static List<Double> elementwiseSubtract(List<Double> left, List<Double> right) {
        return elementwise(left, right, (x, y) -> x - y);
    }

    /**
     * Compounds the list of values.
     *
     * @param values the values to compound.
     * @return a list of values compounded together.
     */
    public static List<Double> compound(List<Double> values) {
        return scan(values, 1.0, Util::compound);
    }

    /**
     * The formula for compounding values. Takes a previous and current value and returns the result of the calculation.
     *
     * @param previous The previous value to compound with.
     * @param current  The current modifier to compound by.
     * @return The result of the compounding calculation.
     */
    public static double compound(double previous, double current) {
        return previous * (current + 1.0);
    }

    /**
     * Runs an operation over a list and creates a resulting list of the running result of the operation.
     *
     * @param list      The list to operate over.
     * @param initial   The initial value to start the operation with.
     * @param operation The operation to perform on the list of values.
     * @param <A>       The type of the values in the original list.
     * @param <B>       The values in the output list.
     * @return The list of values calculated by the scan.
     */
    public static <A, B> List<B> scan(List<A> list, B initial, BiFunction<B, A, B> operation) {
        var result = new ArrayList<B>(list.size());
        var accumulator = initial;

        for (A a : list) {
            accumulator = operation.apply(accumulator, a);
            result.add(accumulator);
        }

        return result;
    }

    public static <A, B> List<B> group(Map<A, B> map, Predicate<A> predicate) {
        var result = new ArrayList<B>();

        for (var entry : map.entrySet()) {
            if (predicate.test(entry.getKey()))
                result.add(entry.getValue());
        }

        return result;
    }


    /**
     * Sums the values in the given list.
     *
     * @param values The values to sum.
     * @return The sum of the values in the list.
     */
    public static Double sum(List<Double> values) {
        var result = values.stream().mapToDouble(i -> i).sum();

        if (Double.isNaN(result))
            throw new ArithmeticException("Sum of values " + values + " resulted in NaN.");

        return result;
    }

    public static <K, A, B, C> Map<K, C> combineMap(Map<K, A> map1, Map<K, B> map2, BiFunction<A, B, C> func) {
        var result = new HashMap<K, C>();
        for (var entry : map1.entrySet()) {
            var key = entry.getKey();
            var value1 = entry.getValue();
            var value2 = map2.get(key);

            result.put(key, func.apply(value1, value2));
        }
        return result;
    }

    public static <K, A, B, C, D> Map<K, D> combineMap(Map<K, A> map1, Map<K, B> map2, Map<K, C> map3, TriFunction<A, B, C, D> func) {
        var result = new HashMap<K, D>();
        for (var entry : map1.entrySet()) {
            var key = entry.getKey();
            var value1 = entry.getValue();
            var value2 = map2.get(key);
            var value3 = map3.get(key);

            result.put(key, func.apply(value1, value2, value3));
        }

        return result;
    }

    public static <K, A, B, C, D, E> Map<K, E> combineMap(
            Map<K, A> map1, Map<K, B> map2, Map<K, C> map3, Map<K, D> map4, QuadFunction<A, B, C, D, E> func
    ) {
        var result = new HashMap<K, E>();
        for (var entry : map1.entrySet()) {
            var key = entry.getKey();
            var value1 = entry.getValue();
            var value2 = map2.get(key);
            var value3 = map3.get(key);
            var value4 = map4.get(key);

            result.put(key, func.apply(value1, value2, value3, value4));
        }
        return result;
    }

    @SuppressWarnings("unchecked")
    public static <K, L, R> Result<Map<K, L>, R> resultSequence(Map<K, Result<L, R>> resultMap) {
        var result = new HashMap<K, L>();

        for (var entry : resultMap.entrySet()) {
            if (entry.getValue() instanceof Success<L, R> success)
                result.put(entry.getKey(), success.value());
            else if (entry.getValue() instanceof Failure<L, R> failure)
                return (Result<Map<K, L>, R>) failure;
        }

        return new Success<>(result);
    }

    public static <L, R> Result<List<L>, R> resultSequence(List<Result<L, R>> results) {
        var result = new ArrayList<L>(results.size());

        for(var value : results) {
            if(value instanceof Result.Success<L,R> success)
                result.add(success.value());
            else if(value instanceof Result.Failure<L,R> failure)
                return (Result<List<L>, R>) failure;
        }

        return new Success<>(result);
    }

    public static <T> T getInstanceFromArgCount(Class<T> clazz, List<Object> args) {
        for (var constructor : clazz.getConstructors()) {
            var parameters = constructor.getParameters();

            if (parameters.length != args.size() || !sameListItemType(parameters, args))
                continue;

            var convertedArrayArgs = convertArrayArgs(parameters, args);

            try {
                return (T) constructor.newInstance(convertedArrayArgs.toArray());
            } catch (InvocationTargetException | InstantiationException | IllegalAccessException e) {
                throw new IllegalArgumentException(
                        "Could not construct instance of type " + clazz.getName() + ". Cause " + e.getCause()
                );
            }
        }

        throw new IllegalArgumentException(
                "Class " + clazz.getName() + " has no constructor with " + args.size() + " parameters "
        );
    }

    private static List<Object> convertArrayArgs(Parameter[] parameters, List<Object> args) {
        var result = new ArrayList<>(args.size());

        for (int i = 0; i < parameters.length; i++) {
            var param = parameters[i];
            var arg = args.get(i);

            if (param.getType().isArray()) {
                if (param.getType().getComponentType().equals(double.class))
                    result.add(Arrays.stream(((Object[]) arg)).map(Object::toString).mapToDouble(Double::valueOf).toArray());
                else if (param.getType().getComponentType().equals(int.class))
                    result.add(Arrays.stream(((Object[]) arg)).map(Object::toString).mapToInt(Integer::valueOf).toArray());
            } else {
                result.add(arg);
            }
        }

        return result;
    }

    public static boolean sameListItemType(Parameter[] parameters, List<Object> args) {
        var parameterClasses = Arrays.stream(parameters).map(Parameter::getType).toList();
        var argClasses = args.stream().map(Object::getClass).toList();

        for (var i = 0; i < parameterClasses.size(); i++) {
            var parameter = parameterClasses.get(i);
            var arg = argClasses.get(i);

            if (!ClassUtils.isAssignable(arg, parameter) && !(parameter.isArray() && arg.isArray()))
                return false;
        }

        return true;
    }

    public static Map<Integer, Set<Integer>> groupByBcn(List<Alternative> alternatives) {
        var result = new HashMap<Integer, Set<Integer>>();

        for (var alternative : alternatives) {
            for (var bcnID : alternative.bcns()) {
                if (!result.containsKey(bcnID))
                    result.put(bcnID, new HashSet<>());

                result.get(bcnID).add(alternative.id());
            }
        }

        return result;
    }
}
