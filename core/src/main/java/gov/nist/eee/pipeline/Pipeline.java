package gov.nist.eee.pipeline;

import org.atteo.classindex.IndexAnnotated;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@IndexAnnotated
@Retention(RetentionPolicy.RUNTIME)
public @interface Pipeline {
    String name() default "";
    boolean internal() default false;
    Class<?>[] dependencies() default {};
    Class<?>[] inputDependencies() default {};
}
