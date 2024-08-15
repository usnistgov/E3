package gov.nist.eee.pipeline;

import gov.nist.eee.object.Model;
import nz.sodium.Cell;

public interface IWithAssignableInputs {
    /**
     * Creates a Model which is a collection of inputs that can alter the current models state.
     *
     * @return a model which contains double and integer input Cell Sinks.
     */
    Cell<Model> getAssignableInputs();
}
