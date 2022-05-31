package gov.nist.e3.util;

import gov.nist.e3.objects.input.VarRate;
import nz.sodium.Lambda1;
import org.apache.commons.lang3.ClassUtils;
import org.jetbrains.annotations.NotNull;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Parameter;
import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import static gov.nist.e3.formula.Formula.compound;

public class Util {
    private Util() {
        throw new IllegalStateException("Cannot instantiate static utility class");
    }

    /**
     * Maps input values by the formula corresponding to the given VarRate. For Year By Year the values are not
     * altered, for Percent Delta the values are compounded throughout the study period.
     *
     * @param values  The values to iterate.
     * @param varRate The Var Rate to determine how to map the values.
     * @return Either the unaltered values or the values compounded over time.
     */
    public static List<Double> mapWithVarRate(@NotNull List<Double> values, @NotNull VarRate varRate) {
        return switch (varRate) {
            case YEAR_BY_YEAR -> values;
            case PERCENT_DELTA -> compound(values);
        };
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
            throw new IllegalArgumentException("Elementwise can only be done on lists of the same size.");

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

    public static List<Double> elementwiseSubtract(List<Double> left, List<Double> right) {
        return elementwise(left, right, (x, y) -> x - y);
    }

    /**
     * Sums the values in the given list.
     *
     * @param values The values to sum.
     * @return The sum of the values in the list.
     */
    public static Double sum(List<Double> values) {
        return values.stream().mapToDouble(i -> i).sum();
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
        return list -> list.stream().collect(Collectors.toMap(keyExtractor, valueExtractor));
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

    public static <A, B> List<B> getIndices(Map<A, B> map, List<A> keys) {
        var result = new ArrayList<B>(keys.size());

        for (var key : keys) {
            if (!map.containsKey(key))
                continue;

            result.add(map.get(key));
        }

        return result;
    }

    public static <A, B> List<B> getIndiciesIf(Map<A, B> map, List<A> keys, Predicate<B> predicate) {
        return getIndices(map, keys).stream().filter(predicate).toList();
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

    public static <A, B, C> Map<C, B> mapKeys(Map<A, B> original, Function<A, C> mapper) {
        var result = new HashMap<C, B>();

        for (var entry : original.entrySet()) {
            result.put(mapper.apply(entry.getKey()), entry.getValue());
        }

        return result;
    }

    public static <A, B, C> Map<A, C> mapValues(Map<A, B> original, Function<B, C> mapper) {
        var result = new HashMap<A, C>();

        for (var entry : original.entrySet()) {
            result.put(entry.getKey(), mapper.apply(entry.getValue()));
        }

        return result;
    }

    public static boolean nonNull(Object... objects) {
        return Arrays.stream(objects).allMatch(Objects::nonNull);
    }

    public static List<Double> inflateVarValue(List<Double> varValue, int size) {
        if (varValue == null)
            throw new IllegalArgumentException("Cannot inflate null array");

        if (varValue.size() == size)
            return varValue;

        if (varValue.size() != 1)
            throw new IllegalArgumentException(
                    "Cannot inflate partially defined var value array. Given " + varValue + " with size " + size
            );

        var result = new ArrayList<Double>(size);
        var value = varValue.get(0);

        result.add(0.0);
        for (int i = 1; i < size; i++) {
            result.add(value);
        }

        return result;
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

    public static boolean isArrayAssignable(Class<?> from, Class<?> to) {
        if (!from.isArray() || !to.isArray())
            throw new IllegalArgumentException("Class is not an Array. Given: " + from + " " + to);

        return ClassUtils.isAssignable(from.getComponentType(), to.getComponentType());
    }

    @SafeVarargs
    public static <A> List<A> createList(A... values) {
        var result = new ArrayList<A>(values.length);
        Collections.addAll(result, values);
        return result;
    }
}