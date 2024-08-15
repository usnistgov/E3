package gov.nist.eee.pipeline;

public interface IMappedPipeline<P, O> extends IPipeline<P> {
    O mapOutput(P created);
}
