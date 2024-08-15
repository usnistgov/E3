package gov.nist.eee.pipeline;

import java.util.HashMap;
import java.util.Map;

public class DependencyParameters {
    private final Map<Class<?>, Object> parameters = new HashMap<>();

    public <T> void add(Class<?> key, T value) {
        parameters.put(key, value);
    }

    @SuppressWarnings("unchecked")
    public <K, V> V get(Class<K> from) {
        return (V) parameters.get(from);
    }

    @Override
    public String toString() {
        return parameters.toString();
    }
}
