package gov.nist.eee.output;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import nz.sodium.Cell;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;
import java.util.function.Function;

public class ResultNonSequenceOutputMapper implements IOutputMapper {
    private static final Logger logger = LoggerFactory.getLogger(ResultNonSequenceOutputMapper.class);

    @Override
    public Cell<Object> outputMapper(Object input) {
        return ((Cell<Result<Map<Integer, Object>, E3Exception>>) input).map(result -> result.on(
                Function.identity(),
                error -> {
                    logger.warn("Could not create output of since it failed with error " + error);
                    return null;
                }
        ));
    }
}
