package gov.nist.eee.pipeline.optional;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.output.IOutputMapper;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import nz.sodium.Cell;

import java.util.List;
import java.util.Map;

public class OptionalOutputMapper implements IOutputMapper {
    @Override
    public Cell<Object> outputMapper(Object input) {
        var in = (Cell<Result<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception >>) input;

        Cell<List<Cell<OptionalCashflow>>> cashflows = in.map(result -> {
            if(result instanceof Result.Success<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception> success) {
                return success.value().values().stream().toList();
            }

            if(result instanceof Result.Failure<Map<OptionalKey, Cell<OptionalCashflow>>, E3Exception> failure) {
                return List.of();
            }

            return List.of();
        });

        return Cell.switchC(cashflows.map(CellUtils::sequence)).map(x -> x);
    }
}
