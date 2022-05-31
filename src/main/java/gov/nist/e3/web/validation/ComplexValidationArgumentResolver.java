package gov.nist.e3.web.validation;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.fge.jackson.JsonLoader;
import com.github.fge.jsonschema.core.exceptions.ProcessingException;
import com.github.fge.jsonschema.main.JsonSchema;
import com.github.fge.jsonschema.main.JsonSchemaFactory;
import gov.nist.e3.web.api.ApiController;
import gov.nist.e3.web.validation.result.ValidationResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.MethodParameter;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.support.WebDataBinderFactory;
import org.springframework.web.context.request.NativeWebRequest;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.method.support.ModelAndViewContainer;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;

public class ComplexValidationArgumentResolver implements HandlerMethodArgumentResolver {
    private static final Logger log = LoggerFactory.getLogger(ApiController.class);

    private final ObjectMapper objectMapper;
    private final JsonSchemaFactory schemaFactory = JsonSchemaFactory.byDefault();
    private final Map<String, JsonSchema> cache = new ConcurrentHashMap<>();

    public ComplexValidationArgumentResolver(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    private JsonSchema getJsonSchema(String schemaPath) {
        return cache.computeIfAbsent(schemaPath, path -> {
            try {
                var schemaNode = JsonLoader.fromResource(schemaPath);
                return schemaFactory.getJsonSchema(schemaNode);
            } catch (ProcessingException | IOException e) {
                throw new RuntimeException(e);
            }
        });
    }

    private String getJsonPayload(NativeWebRequest nativeWebRequest) throws IOException {
        var httpServletRequest = nativeWebRequest.getNativeRequest(HttpServletRequest.class);
        return StreamUtils.copyToString(httpServletRequest.getInputStream(), StandardCharsets.UTF_8);
    }

    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        return parameter.getParameterAnnotation(ComplexValidation.class) != null;
    }

    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {
        var schemaPath = parameter.getParameterAnnotation(ComplexValidation.class).withJsonSchema();
        var json = objectMapper.readTree(getJsonPayload(webRequest));

        if(!schemaPath.equals("")) {
            var schema = getJsonSchema(schemaPath);
            var result = schema.validate(json);

            if (!result.isSuccess())
                throw new RuntimeException(result.toString());
        }

        var obj = objectMapper.treeToValue(json, parameter.getParameterType());

        var results = Arrays.stream(parameter.getParameterType().getMethods())
                .filter(method -> method.getAnnotation(ComplexValidationTest.class) != null && method.getReturnType() == ValidationResult.class)
                .map(method -> {
                    try {
                        return (ValidationResult) method.invoke(obj);
                    } catch (IllegalAccessException | InvocationTargetException e) {
                        throw new RuntimeException("Could not run validation test method", e);
                    }
                })
                .filter(r -> r instanceof ValidationResult.Failure)
                .toList();

        if(!results.isEmpty()) {
            results.forEach(r -> log.debug(((ValidationResult.Failure) r).getMessage()));
            throw new RuntimeException("Validation failed");
        }
        return obj;
    }
}
