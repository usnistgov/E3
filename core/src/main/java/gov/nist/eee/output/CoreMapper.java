package gov.nist.eee.output;

import gov.nist.eee.util.CellUtils;
import nz.sodium.Cell;

import java.util.Map;

public class CoreMapper implements IOutputMapper {
    @Override
    public Cell<Object> outputMapper(Object input) {
        return Cell.switchC(((Cell<Map<Integer, Cell<Object>>>) input).map(CellUtils::sequenceMap)).map(x -> x);
    }
}
