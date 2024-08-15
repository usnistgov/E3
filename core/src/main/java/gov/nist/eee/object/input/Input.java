package gov.nist.eee.object.input;

import java.util.List;
import java.util.Map;

public record Input(
        Analysis analysis,
        List<Alternative> alternativeObjects,
        List<Bcn> bcnObjects,
        Map<String, Object> extensions
){
}
