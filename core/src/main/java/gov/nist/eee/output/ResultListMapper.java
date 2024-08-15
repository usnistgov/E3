package gov.nist.eee.output;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.util.Result;
import nz.sodium.Cell;

import java.util.List;

public class ResultListMapper implements IOutputMapper {
    @Override
    public Cell<Object> outputMapper(Object input) {
        return ((Cell<Result<List<Object>, E3Exception>>) input).map(result -> {
            if (result instanceof Result.Success<List<Object>, E3Exception> success) {
                return success.value();
            }

            throw new RuntimeException("Could not create output since result is failure");
        });
    }
}