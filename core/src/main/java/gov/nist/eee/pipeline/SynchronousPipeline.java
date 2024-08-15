package gov.nist.eee.pipeline;

public abstract class SynchronousPipeline<T> implements IPipeline<T> {
    public abstract T run();
}
