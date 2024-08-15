package gov.nist.eee.object.input;

import java.util.List;

public record Bcn (
    int id,
    //List<Integer> altIds,
    BcnType type,
    BcnSubType subType,
    String name,
    List<String> tags,
    int initialOccurrence,
    boolean real,
    boolean invest,
    Integer life,
    boolean residualValue,
    boolean residualValueOnly,
    RecurOptions recur,
    Double quantityValue,
    double quantity,
    VarRate quantityVarRate,
    List<Double> quantityVarValue,
    String quantityUnit
){}

