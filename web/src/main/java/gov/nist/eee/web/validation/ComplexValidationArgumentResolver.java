package gov.nist.eee.web.validation;

import com.fasterxml.jackson.databind.ObjectMapper;
import gov.nist.eee.validation.JsonSchemaValidator;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.MethodParameter;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.support.WebDataBinderFactory;
import org.springframework.web.context.request.NativeWebRequest;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.method.support.ModelAndViewContainer;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;

public class ComplexValidationArgumentResolver implements HandlerMethodArgumentResolver {
    private static final Logger log = LoggerFactory.getLogger(ComplexValidationArgumentResolver.class);

    private final ObjectMapper objectMapper;

    public ComplexValidationArgumentResolver(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
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
        var schema = parameter.getParameterAnnotation(ComplexValidation.class).withJsonSchema();

        var validator = new JsonSchemaValidator(objectMapper, Path.of(schema));
        return validator.validate(getJsonPayload(webRequest), parameter.getParameterType());
    }
}
