package gov.nist.eee.cli;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.MapperFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;
import gov.nist.eee.object.input.Input;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

@Command(name = "e3", mixinStandardHelpOptions = true, version = "E3 alpha-2.0", description = "General use economic evaluation engine.")
public class E3 implements Runnable {
    private static final Logger logger = LoggerFactory.getLogger(E3.class);
    @Parameters(index = "0", description = "JSON file with E3 options.")
    private File input;

    @Option(names = {"-o, --output"}, description = "Output file path.")
    private File output;

    private final ObjectMapper mapper;
    private final JsonSchemaFactory factory = JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V202012);

    public E3() {
        mapper = JsonMapper.builder()
                .configure(MapperFeature.ACCEPT_CASE_INSENSITIVE_ENUMS, true)
                .configure(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY, true)
                .build();
    }

    @Override
    public void run() {
        try (
                var validationStream = Files.newInputStream(input.toPath());
                var inputStream = Files.newInputStream(input.toPath());
        ) {
            var inputNode = mapper.readTree(validationStream);
            var schema = factory.getSchema(
                    Thread.currentThread().getContextClassLoader().getResourceAsStream("e3-request-schema.json")
            );

            var errors = schema.validate(inputNode);

            if (!errors.isEmpty())
                logger.error(errors.toString());

            System.out.println("Checkpoint");

            var inputObject = mapper.readValue(inputStream, Input.class);

            var e3 = new gov.nist.eee.E3();
            e3.addListener(System.out::println);
            e3.analyze(inputObject);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        var exitCode = new CommandLine(new E3()).execute(args);
        System.exit(exitCode);
    }
}
