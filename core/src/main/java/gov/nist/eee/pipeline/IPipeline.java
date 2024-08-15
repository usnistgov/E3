package gov.nist.eee.pipeline;

import gov.nist.eee.object.input.Input;
import nz.sodium.Cell;
import nz.sodium.Stream;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.ServiceLoader;

public interface IPipeline<P> {
    static List<IPipeline<?>> getInstances() {
        var services = ServiceLoader.load(IPipeline.class);

        var result = new ArrayList<IPipeline<?>>();
        services.iterator().forEachRemaining(result::add);
        return result;
    }

    /**
     * Configures any member variables that can be derived from the main input stream.
     *
     * @param sInput     the main input stream which contains Input objects.
     */
    void setup(final Stream<Input> sInput);
}
