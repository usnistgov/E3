package clone;

import gov.nist.eee.object.input.Bcn;
import gov.nist.eee.object.input.BcnSubType;
import gov.nist.eee.object.input.BcnType;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class CloneTest {

    private static Bcn bcnRecord = new Bcn(
            0,
            List.of(0),
            BcnType.COST,
            BcnSubType.DIRECT,
            "Bcn 1",
            null,
            0,
            true,
            false,
            5,
            false,
            false,
            null,
            0.05,
            100,
            null,
            null,
            null
    );

    /**
     * {@link Clone#clone(Record)} should return a different object instance.
     */
    @Test
    void differentObject() {
        var cloned = Clone.clone(bcnRecord);

        assertNotSame(bcnRecord, cloned);
    }

    /**
     * {@link Clone#clone(Record)} should return an object where the fields are equal.
     */
    @Test
    void sameElements() {
        var cloned = Clone.clone(bcnRecord);

        assertEquals(bcnRecord, cloned);
    }

    /**
     * {@link Clone#clone(Record, Map)} with a given map should return an object with all fields the same except for
     * the ones specified in the map.
     */
    @Test
    void alteredField() {
        var cloned = Clone.clone(bcnRecord, Map.of("quantity", 582));

        assertNotEquals(bcnRecord, cloned);
        assertEquals(582, cloned.quantity());
    }
}