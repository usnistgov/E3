package gov.nist.eee.web;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.Module;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.module.SimpleModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * Custom serializer for ensuring double values are outputted in expanded form and not shortened with e notation.
 */
@Configuration
public class ExpandedDoubleSerializerConfig {
    public static class ExpandedDoubleSerializer extends JsonSerializer<Double> {
        @Override
        public void serialize(Double value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
            if(value.isNaN() || value.isInfinite())
                gen.writeNumber(value);
            else
                gen.writeNumber(BigDecimal.valueOf(value).toPlainString());
        }
    }

    @Bean
    public Module expandedDoubleModule() {
        var serializer = new ExpandedDoubleSerializer();
        var module = new SimpleModule();

        module.addSerializer(double.class, serializer);
        module.addSerializer(Double.class, serializer);

        return module;
    }
}
