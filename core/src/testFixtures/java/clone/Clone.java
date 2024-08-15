package clone;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.RecordComponent;
import java.util.Arrays;
import java.util.Map;
import java.util.stream.Collectors;

public class Clone {
    private Clone() {
        throw new UnsupportedOperationException("Cannot instantiate static utility class");
    }

    public static <T extends Record> T clone(T obj) {
        return clone(obj, Map.of());
    }

    @SuppressWarnings("unchecked")
    public static <T extends Record> T clone(T obj, Map<String, ?> with) {
        var cls = obj.getClass();
        var accessors = Arrays.stream(cls.getRecordComponents())
                .collect(Collectors.toMap(RecordComponent::getName, RecordComponent::getAccessor));
        var constructor = cls.getConstructors()[0];
        var parameters = constructor.getParameters();

        var parameterValues = Arrays.stream(parameters).map(p -> {
            var name = p.getName();

            if(with.containsKey(name))
                return with.get(name);

            try {
                return accessors.get(name).invoke(obj);
            } catch (IllegalAccessException | InvocationTargetException e) {
                throw new RuntimeException(e);
            }
        }).toArray();

        try {
            return (T) constructor.newInstance(parameterValues);
        } catch (InstantiationException | IllegalAccessException | InvocationTargetException e) {
            throw new RuntimeException(e);
        }
    }
}
