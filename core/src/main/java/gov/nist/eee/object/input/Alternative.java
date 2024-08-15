package gov.nist.eee.object.input;

import java.util.List;

public record Alternative(int id, String name, List<Integer> bcns) {
}
