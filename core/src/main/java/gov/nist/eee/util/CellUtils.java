package gov.nist.eee.util;

import gov.nist.eee.E3;
import gov.nist.eee.error.E3Exception;
import nz.sodium.*;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;
import java.util.stream.Collectors;

public class CellUtils {
    public static <A> Stream<A> calm(Stream<A> sA, Lazy<Optional<A>> oInit) {
        return Stream.filterOptional(sA.collectLazy(oInit, (A a, Optional<A> oLastA) -> {
            Optional<A> oa = Optional.of(a);
            return oa.equals(oLastA) ? new Tuple2<>(Optional.empty(), oLastA) : new Tuple2<>(oa, oa);
        }));
    }

    public static <A> Stream<A> calm(Stream<A> sA) {
        return calm(sA, new Lazy<>(Optional.empty()));
    }

    public static <A> Cell<A> calm(Cell<A> a) {
        Lazy<A> initA = a.sampleLazy();
        Lazy<Optional<A>> oInitA = initA.map(Optional::of);
        return calm(Operational.updates(a), oInitA).holdLazy(initA);
    }

    public static <A> Cell<A> withCleanup(Cell<A> a, Consumer<A> cleanup) {
        return Operational.updates(a).accum(a.sample(), (current, previous) -> {
            if (previous != null) cleanup.accept(previous);

            return current;
        });
    }

    public static <A> Cell<A> tap(Cell<A> cell, Consumer<A> consumer) {
        return cell.map(a -> {
            consumer.accept(a);
            return a;
        });
    }

    public static <A> Lambda1<A, A> tap(Consumer<A> consumer) {
        return a -> {
            consumer.accept(a);
            return a;
        };
    }

    public static <A> Cell<A> or(Cell<Boolean> predicate, Cell<A> left, Cell<A> right) {
        return Cell.switchC(predicate.map(p -> Boolean.TRUE.equals(p) ? left : right));
    }

    public static <A> Cell<A> or(boolean predicate, Cell<A> left, Cell<A> right) {
        return predicate ? left : right;
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
        if (cells.isEmpty()) return new Cell<>(List.of());

        // Base case, if there is only one cell in the list, map it into an arraylist and return.
        if (cells.size() == 1) return cells.get(0).map(value -> {
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
        if (cells.size() <= 1) return cells.get(0);

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

    public static <K, V> Cell<Map<K, V>> sequenceMap(Map<K, Cell<V>> map) {
        if (map == null || map.isEmpty()) return new Cell<>(new HashMap<>());

        if (map.size() == 1) {
            var entry = map.entrySet().stream().findFirst().get();

            return entry.getValue().map(value -> {
                if (value == null) return new HashMap<>();

                var result = new HashMap<K, V>();
                result.put(entry.getKey(), value);
                return result;
            });
        }

        var entries = map.entrySet().stream().toList();

        var middle = entries.size() / 2;

        var left = entries.subList(0, middle).stream().collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
        var right = entries.subList(middle, entries.size()).stream().collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

        return sequenceMap(left).lift(sequenceMap(right), (l, r) -> {
            var result = new HashMap<K, V>(l.size() + r.size());

            result.putAll(l);
            result.putAll(r);

            return result;
        });
    }

    public static <A> Stream<A> gate(Cell<A> cValue, Cell<Boolean> cBoolean) {
        return Operational.updates(cValue).gate(cBoolean);
    }

    public static <A> Stream<A> ignore(int ignore, Stream<A> sValues) {
        AtomicInteger i = new AtomicInteger();

        var result = new StreamSink<A>();
        sValues.listen(a -> {
            if (i.get() >= ignore) Transaction.post(() -> result.send(a));
            else i.getAndIncrement();
        });
        return result;
    }

    public static <T> Cell<Result<T, E3Exception>> wrapError(E3Exception error) {
        return new Cell<>(new Result.Failure<>(error));
    }
}
