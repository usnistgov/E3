package gov.nist.e3.util;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.function.Consumer;
import java.util.function.Supplier;

public class Pool<T> {
    private final Deque<T> reserve = new ArrayDeque<>();

    private final Consumer<T> cleanup;
    private final Supplier<T> constructor;

    private final int maxSize;

    public Pool(int maxSize, Supplier<T> constructor, Consumer<T> cleanup) {
        this.maxSize = maxSize;
        this.cleanup = cleanup;
        this.constructor = constructor;
    }

    public T get() {
        if(!reserve.isEmpty())
            return reserve.pop();

        return constructor.get();
    }

    public void release(T t) {
        if (reserve.size() >= maxSize)
            return;

        cleanup.accept(t);
        reserve.add(t);
    }
}
