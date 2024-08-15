package gov.nist.eee.pipeline;

import nz.sodium.Cell;

public abstract class CellPipeline<T> implements IPipeline<T> {
    /**
     * Defines the result of the pipeline.
     *
     * @return a cell that contains the output of the pipeline for any Input that arrives in the main input stream.
     */
    public abstract Cell<T> define();
}
