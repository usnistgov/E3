package gov.nist.eee.object.input;

import java.util.List;

public record RecurOptions (
    int interval,
    VarRate varRate,
    List<Double> varValue,
    Integer end
){}
