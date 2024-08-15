package gov.nist.eee.pipeline;

import gov.nist.eee.object.Model;
import nz.sodium.Cell;

import java.util.Map;

public interface IWithInput {
    void setupInput(Cell<Model> cModel);
}
