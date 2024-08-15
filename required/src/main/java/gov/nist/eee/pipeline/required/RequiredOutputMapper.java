package gov.nist.eee.pipeline.required;

import gov.nist.eee.error.E3Exception;
import gov.nist.eee.output.IOutputMapper;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import nz.sodium.Cell;

import java.util.List;
import java.util.Map;

public class RequiredOutputMapper implements IOutputMapper {
    @Override
    public Cell<Object> outputMapper(Object input) {
        var in = (Cell<Result<Map<Integer, Cell<RequiredCashflow>>, E3Exception>>) input;

        Cell<List<Cell<RequiredCashflow>>> cashflows = in.map(result -> {
            if(result instanceof Result.Success<Map<Integer, Cell<RequiredCashflow>>, E3Exception> success) {
                return success.value().values().stream().toList();
            }

            if(result instanceof Result.Failure<Map<Integer, Cell<RequiredCashflow>>, E3Exception> failure) {
                return List.of();
            }

            return List.of();
        });

        return Cell.switchC(cashflows.map(CellUtils::sequence)).map(x -> x);
    }
}
