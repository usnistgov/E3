package gov.nist.e3.util;

import nz.sodium.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

/**
 * Provides utility functions for operations on Sodium Cells.
 */
public class CellUtils {
    private CellUtils() {
        throw new IllegalStateException("Cannot instantiate static utility class");
    }

    /**
     * Merges a list of cells into a single cell. The operation is done with a balanced tree so any individual
     * update to one of the cells will update its dependencies in O(log(n)) time.
     *
     * @param combiner Function that combines two cells.
     * @param cells    The list of cells to combine.
     * @param <T>      The type contained within the cells.
     * @return A single cell containing the combined values from the given cells.
     */
    public static <T> Cell<T> mergeList(final Lambda2<T, T, T> combiner, final List<? extends Cell<T>> cells) {
        // Base case, if there is only one cell, return its value.
        if (cells.size() <= 1)
            return cells.get(0);

        var newCells = new ArrayList<Cell<T>>((cells.size() + 1) / 2);

        // Combine every other cell with its neighbor.
        for (int i = 0; i < cells.size() - 1; i += 2) {
            newCells.add(cells.get(i).lift(cells.get(i + 1), combiner));
        }

        // Add the last cell without combining if there is an odd number of cells.
        if (cells.size() % 2 == 1) {
            newCells.add(cells.get(cells.size() - 1));
        }

        // Recurse with the list of partially combined cells.
        return mergeList(combiner, newCells);
    }

    /**
     * Flattens a list of cells into a cell containing a list of values previously containing in the given cells.
     *
     * @param cells The list of cells to flatten.
     * @param <T>   The type contained within the cells.
     * @return A cell containing a list of values taken from the given list of cells. This list will update whenever
     * one of its constituent cells updates.
     */
    public static <T> Cell<List<T>> sequence(List<? extends Cell<T>> cells) {
        if (cells.isEmpty())
            return new Cell<>(List.of());

        // Base case, if there is only one cell in the list, map it into an arraylist and return.
        if (cells.size() == 1)
            return cells.get(0).map(value -> {
                var result = new ArrayList<T>();
                result.add(value);
                return result;
            });

        var middle = cells.size() / 2;

        var left = cells.subList(0, middle);
        var right = cells.subList(middle, cells.size());

        // Recursively flatten the left and right sublists and then combine the results into a single list.
        return sequence(left).lift(sequence(right), (l, r) -> {
            var result = new ArrayList<T>(l.size() + r.size());

            result.addAll(l);
            result.addAll(r);

            return result;
        });
    }

    public static <A, B, C> Lambda1<A, C> compose(Lambda1<A, B> f1, Lambda1<B, C> f2) {
        return a -> f2.apply(f1.apply(a));
    }

    public static <A, S> Stream<Lambda1<S, S>> change(Stream<A> value, BiFunction<S, A, S> stateFunction) {
        return value.map(a -> s -> stateFunction.apply(s, a));
    }

    @SafeVarargs
    public static <S> Cell<S> state(S initial, Stream<Lambda1<S, S>>... changes) {
        return Transaction.run(() -> {
            var state = new CellLoop<S>();
            var composedChanges = Stream.merge(Arrays.asList(changes), CellUtils::compose);

            state.loop(composedChanges.snapshot(state, Lambda1::apply).hold(initial));

            return state;
        });
    }

    public static <A, B> Cell<@Nullable B> nullableFlatMap(@NotNull Cell<@Nullable A> nullable, Function<@NotNull A, Cell<B>> mapper) {
        return Cell.switchC(nullable.map(v -> v == null ? new Cell<>(null) : mapper.apply(v)));
    }

    public static <A, B> Cell<B> nullableMap(@NotNull Cell<@Nullable A> nullable, Function<@NotNull A, B> mapper) {
        return nullable.map(v -> v == null ? null : mapper.apply(v));
    }

    public static <A> Cell<@Nullable A> liftNullable(@Nullable A nullableValue) {
        return liftNullable(nullableValue, x -> x);
    }

    public static <A, B> Cell<@Nullable B> liftNullable(@Nullable A nullableValue, Function<@NotNull A, B> mapper) {
        if (nullableValue == null)
            return new Cell<>(null);

        return new Cell<>(mapper.apply(nullableValue));
    }

    public static <A, B> Cell<@Nullable B> gate(Cell<A> gateCell, Predicate<A> predicate, Supplier<Cell<B>> resultSupplier) {
        return Cell.switchC(gateCell.map(v -> predicate.test(v) ? resultSupplier.get() : new Cell<>(null)));
    }
}
