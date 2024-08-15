package gov.nist.eee.pipeline;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface OutputMapper {
    Class<?> value();
}
