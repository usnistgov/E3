package gov.nist.eee.output;

import nz.sodium.Cell;

public interface IOutputMapper {
    Cell<Object> outputMapper(Object input);
}
