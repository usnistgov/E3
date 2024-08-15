package gov.nist.eee.validation;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

class JsonSchemaValidatorTest {
    static ObjectMapper mapper;

    @BeforeAll
    static void setup() {
        mapper = new ObjectMapper();
    }

    @Test
    void testValidObject() {
        JsonSchemaValidator validator = new JsonSchemaValidator(mapper, Path.of("/test-schema-1.json"));
        TestObject value = validator.validate("{\"property1\": 10}", TestObject.class);

        assertNotNull(value);
    }

    @Test
    void testInvalidObject() {
        JsonSchemaValidator validator = new JsonSchemaValidator(mapper, Path.of("/test-schema-1.json"));
        assertThrows(RuntimeException.class, () -> validator.validate("\"property2\": \"Hello\"}", TestObject.class));
    }
}