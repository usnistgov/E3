package gov.nist.eee.validation;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;
import com.networknt.schema.ValidationMessage;

import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Path;
import java.util.Set;

public class JsonSchemaValidator {
    private final ObjectMapper objectMapper;
    private final JsonSchema schema;

    private final JsonSchemaFactory schemaFactory = JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V201909);

    public JsonSchemaValidator(final ObjectMapper objectMapper, final Path schemaPath) {
        this.objectMapper = objectMapper;
        this.schema = getJsonSchema(schemaPath);
    }

    public JsonSchemaValidator(final ObjectMapper objectMapper, final InputStream schemaStream) {
        this.objectMapper = objectMapper;
        this.schema = getJsonSchema(schemaStream);
    }

    private JsonSchema getJsonSchema(InputStream schema) {
        return schemaFactory.getSchema(schema);
    }

    private JsonSchema getJsonSchema(Path schemaPath) {
        return getJsonSchema(this.getClass().getResourceAsStream(schemaPath.toString()));
    }

    public Set<ValidationMessage> validate(JsonNode node) {
        return schema.validate(node);
    }

    public <T> T validate(String json, Class<T> clazz) {
        try {
            var jsonNode = objectMapper.readTree(json);
            var result = schema.validate(jsonNode);

            if (!result.isEmpty())
                throw new RuntimeException(result.toString());

            var obj = objectMapper.treeToValue(jsonNode, clazz);
            var testResult = runValidationTests(obj);

            if (!testResult) {
                throw new RuntimeException("Additional validation tests failed");
            }

            return obj;
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private <T> boolean runValidationTests(T instance) {
        for (var method : instance.getClass().getMethods()) {
            if (method.getAnnotation(ValidationTest.class) == null | method.getReturnType() != Result.class)
                continue;

            try {
                var result = (Result) method.invoke(instance);

                if (!(result instanceof Result.Success))
                    return false;
            } catch (InvocationTargetException | IllegalAccessException e) {
                throw new RuntimeException(e);
            }
        }

        return true;
    }
}
