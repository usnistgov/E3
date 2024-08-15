package gov.nist.eee.web.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.networknt.schema.ValidationMessage;
import gov.nist.eee.E3;
import gov.nist.eee.Subscription;
import gov.nist.eee.object.input.Alternative;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Bcn;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.util.Result;
import gov.nist.eee.validation.JsonSchemaValidator;
import gov.nist.eee.web.exceptions.ApiTokenException;
import gov.nist.eee.tuple.Tuple2;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.request.async.DeferredResult;

import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ForkJoinPool;

/**
 * Spring controller that contains API endpoints.
 */
@RestController
@Validated
@RequestMapping("/api/v2")
public class ApiController {
    private static final Logger log = LoggerFactory.getLogger(ApiController.class);

    /**
     * Encoder for hashing and checking the API tokens. The BCrypt encoder is used which automatically salts encoded
     * strings.
     */
    private static final BCryptPasswordEncoder ENCODER = new BCryptPasswordEncoder();

    private final ApiTokenRepository repository;

    public E3 e3 = new E3();

    private final ObjectMapper mapper;

    private final JsonSchemaValidator mainValidator;
    private HashMap<String, Tuple2<JsonSchemaValidator, JavaType>> extensions;

    public ApiController(ApiTokenRepository repository, ObjectMapper mapper) {
        this.mapper = mapper;
        this.repository = repository;

        this.mainValidator = new JsonSchemaValidator(mapper, e3.getValidationSchema());

        /*e3.cSchemaStreams.map(m -> {
            var result = new HashMap<String, JsonSchemaValidator>();
            for (var entry : m.entrySet()) {
                result.put(entry.getKey(), new JsonSchemaValidator(mapper, entry.getValue()));
            }
            return result;
        }).listen(x -> extensionValidators = x);*/

        e3.cInputExtensions.map(extensions -> {
            var result = new HashMap<String, Tuple2<JsonSchemaValidator, JavaType>>();

            for (var entry : extensions.entrySet()) {
                var annotation = entry.getValue();
                var clazz = entry.getKey();

                var type = getExtensionType(mapper, clazz, annotation.container());

                var inputStream = clazz.getResourceAsStream(annotation.schema());
                var validator = new JsonSchemaValidator(mapper, inputStream);

                result.put(annotation.key(), new Tuple2<>(validator, type));
            }

            System.out.println("Extensions " + result.toString());

            return result;
        }).listen(result -> {
            extensions = result;
        });
    }

    private JavaType getExtensionType(final ObjectMapper mapper, final Class<?> type, final Class<?> containerType) {
        if (containerType.equals(Void.class))
            return mapper.getTypeFactory().constructType(type);

        return mapper.getTypeFactory().constructParametricType(containerType, type);
    }

    private Result<JsonNode, Set<ValidationMessage>> validateMainNode(final String payload) {
        try {
            var payloadJsonNode = mapper.readTree(payload);
            var mainValidationResult = mainValidator.validate(payloadJsonNode);
            log.debug("Main validation " + mainValidationResult);

            if (!mainValidationResult.isEmpty()) return new Result.Failure<>(mainValidationResult);

            return new Result.Success<>(payloadJsonNode);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private Result<Map<String, JsonNode>, Set<ValidationMessage>> validateExtensions(final JsonNode node) {
        var type = mapper.getTypeFactory().constructMapType(HashMap.class, String.class, JsonNode.class);

        try {
            Map<String, JsonNode> jsonProperties = mapper.treeToValue(node, type);
            log.debug(jsonProperties.toString());

            for (var entry : jsonProperties.entrySet()) {
                var propertyName = entry.getKey();
                var propertyNode = entry.getValue();

                if (!extensions.containsKey(propertyName)) continue;

                log.debug("Validating " + propertyName);
                log.debug(propertyNode.toString());

                var validationResult = extensions.get(propertyName).e1().validate(propertyNode);

                log.debug(propertyName + " validation result " + validationResult);

                if (!validationResult.isEmpty()) return new Result.Failure<>(validationResult);
            }

            return new Result.Success<>(jsonProperties);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private Input createInputObject(final Map<String, JsonNode> properties) {
        // Construct Input Object
        var bcnType = mapper.getTypeFactory().constructCollectionLikeType(ArrayList.class, Bcn.class);
        var alternativeType = mapper.getTypeFactory().constructCollectionLikeType(ArrayList.class, Alternative.class);

        try {
            // Deserialize default objects
            var analysisObject = mapper.treeToValue(properties.get("analysisObject"), Analysis.class);
            List<Alternative> alternativeObjects = mapper.treeToValue(properties.get("alternativeObjects"), alternativeType);
            List<Bcn> bcnObjects = mapper.treeToValue(properties.get("bcnObjects"), bcnType);

            // Deserialize extension objects
            var deserializedExtensions = new HashMap<String, Object>();
            for (var entry : properties.entrySet()) {
                var property = entry.getKey();
                var node = entry.getValue();

                if (property.equals("analysisObject")
                        || property.equals("bcnObjects")
                        || property.equals("alternativeObjects"))
                    continue;

                var tuple = extensions.get(property);

                if(tuple == null) {
                    log.warn("Propety: \"" + property + "\" does not have a validator, ignoring.");
                    continue;
                }

                deserializedExtensions.put(property, mapper.treeToValue(node, tuple.e2()));
            }

            return new Input(analysisObject, alternativeObjects, bcnObjects, deserializedExtensions);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private void checkApiToken(final String authorization) {
        // Check header format
        if (!authorization.startsWith("Api-Key: ")) throw new ApiTokenException("API key header format is invalid");

        // Check UUID format
        String token;
        String prefix;
        try {
            var unparsed = authorization.replace("Api-Key: ", "");
            var split = unparsed.split("\\.");

            if (split.length < 2) throw new ApiTokenException("Token is not in format \"prefix.uuid\"");

            prefix = split[0];
            token = split[1];
        } catch (IllegalArgumentException e) {
            throw new ApiTokenException("API token not in correct format");
        }

        var apiToken = repository.getByPrefix(prefix);

        // Check if token exists in database
        if (apiToken == null) throw new ApiTokenException("API key is invalid");

        // Check if token matches hashed key
        if (!ENCODER.matches(token, apiToken.getToken()))
            throw new ApiTokenException("Prefix exists, but token is incorrect");

        // Check if token is expired
        @Nullable var expiry = apiToken.getExpiry();
        if (expiry != null && expiry.isBefore(LocalDateTime.now())) throw new ApiTokenException("API key is expired");

        // Check if token has been revoked
        if (apiToken.isRevoked()) throw new ApiTokenException("API key has been revoked");
    }

    private DeferredResult<Map<String, Object>> sendInput(final E3 e3, final DeferredResult<Map<String, Object>> output, final Input input) {
        log.debug("RUNNING E3");

        ForkJoinPool.commonPool().submit(() -> {
            Subscription subscription = null;
            var now = System.currentTimeMillis();
            try {
                var result = e3.analyze(input);
                output.setResult(result);
            } catch (Exception e) {
                e.printStackTrace();
                output.setErrorResult(e.getMessage());
            } finally {
                if (subscription != null) subscription.unsubscribe();
            }
            log.info("E3 took {}ms.", System.currentTimeMillis() - now);
        });

        return output;
    }

    /**
     * This is the main API resource of E3 that takes the JSON request and sends it to the calculation engine.
     * Takes the JSON input as a request body and the authorization header. Only a valid API token will be authorized
     * to use this endpoint.
     *
     * @param payload       the E3 input obtained from the request POST body.
     * @param authorization the authorization header that must contain a valid API token in the format
     *                      "Api-Key prefix.token";
     * @return a deferred result that will return the output generated by the E3 engine.
     */
    @CrossOrigin
    @PostMapping("/analysis")
    public DeferredResult<Map<String, Object>> analysis(@RequestBody String payload, @RequestHeader String authorization) {
        log.info("Analysis called");

        checkApiToken(authorization);

        log.info("API token accepted");

        // Pass input to E3 engine and return as deferred result
        var output = new DeferredResult<Map<String, Object>>();

        // Validate and create input object
        var inputResult = validateMainNode(payload).flatMap(this::validateExtensions).map(this::createInputObject);

        log.info("Payload validated");

        if (inputResult instanceof Result.Success<Input, Set<ValidationMessage>> success) {
            return sendInput(e3, output, success.value());
        } else if (inputResult instanceof Result.Failure<Input, Set<ValidationMessage>> failure) {
            output.setErrorResult(failure.error());
            return output;
        } else {
            output.setErrorResult("Could not run E3, try again later");
            return output;
        }
    }
}
