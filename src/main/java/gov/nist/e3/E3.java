package gov.nist.e3;

import gov.nist.e3.compute.MainPipeline;
import gov.nist.e3.objects.input.Input;
import gov.nist.e3.objects.output.Output;
import nz.sodium.Cell;
import nz.sodium.StreamSink;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main object that contains the computation model and analyze method.
 */
public class E3 {
    private static final Logger log = LoggerFactory.getLogger(E3.class);

    /**
     * The input stream that initiates a calculation.
     */
    private final StreamSink<Input> sInput = new StreamSink<>();

    /**
     * A cell containing the output of the calculation.
     */
    private final Cell<Output> cOutput;

    public E3() {
        var pipeline = new MainPipeline(sInput);
        this.cOutput = null;//pipeline.cOutput;
    }

    /**
     * Runs an E3 analysis on the given input and returns the output object.
     *
     * @param input The input to run the analysis on.
     * @return The output object created by the analysis.
     */
    public Output analyze(Input input) {
        sInput.send(input);
        return cOutput.sample();
    }

    /**
     * Runs an E3 analysis on the given input and returns the output object. This is a static function so objects are
     * completely destroyed after analyzing the given input.
     *
     * @param input The input to run the analysis on.
     * @return The output object created by the analysis.
     */
    public static Output analysis(Input input) {
        log.info("Received new request");
        log.debug("Input: {}", input);

        var sInput = new StreamSink<Input>();
        var pipeline = new MainPipeline(sInput);

        // Send input to calculate initial model state
        sInput.send(input);

        // Create and return output object with sampled results.
        return new Output(
                pipeline.required(),
                pipeline.optional(),
                pipeline.measures(),
                pipeline.sensitivity(),
                pipeline.uncertainty()
        );
    }
}
