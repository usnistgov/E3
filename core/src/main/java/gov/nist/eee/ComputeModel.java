package gov.nist.eee;

import com.github.dexecutor.core.DefaultDexecutor;
import com.github.dexecutor.core.DexecutorConfig;
import com.github.dexecutor.core.ExecutionConfig;
import com.github.dexecutor.core.task.Task;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.object.tree.Tree;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.SameThreadExecutorService;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.StreamSink;
import nz.sodium.Transaction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class ComputeModel {
    private static final Logger logger = LoggerFactory.getLogger(ComputeModel.class);
    private Cell<List<String>> cRequestedOutputs;
    private Cell<Map<String, Object>> cOutputs;
    private final Map<Class<?>, SynchronousPipeline<?>> synchronousPipelines = new HashMap<>();

    public ComputeModel(StreamSink<Input> sInput, Cell<List<IPipeline<?>>> cPipelines) {
        logger.trace("Creating compute model");

        Transaction.runVoid(() -> initialize(cPipelines, sInput));
    }

    private void initialize(Cell<List<IPipeline<?>>> cPipelines, StreamSink<Input> sInput) {
        // Run main setup and define pipelines
        Cell<Map<Class<?>, Cell<?>>> definitions = cPipelines.map(pipeline -> setup(pipeline, sInput));
    }

    public Map<Class<?>, Cell<?>> setup(List<IPipeline<?>> toSetup, StreamSink<Input> sInput) {
        logger.debug("Setting up pipelines");

        Map<Class<?>, Cell<Model>> modelCache = new ConcurrentHashMap<>();
        var result = new ConcurrentHashMap<Class<?>, Cell<?>>();
        var pipelines = toSetup.stream().collect(Collectors.toMap(x -> x.getClass(), x -> x));
        synchronousPipelines.clear();

        var config = new DexecutorConfig<Class<?>, IPipeline<?>>(new SameThreadExecutorService(), pipelineClass -> new Task<>() {
            @Override
            public IPipeline<?> execute() {
                var pipeline = pipelines.get(pipelineClass);
                pipeline.setup(sInput);

                if (pipeline instanceof IWithAssignableInputs assignableInputPipeline)
                    modelCache.put(assignableInputPipeline.getClass(), assignableInputPipeline.getAssignableInputs());

                if (pipeline instanceof IWithDependency dependentPipeline) {
                    var dependencies = dependentPipeline.getClass().getAnnotation(Pipeline.class).dependencies();
                    var parameters = new DependencyParameters();

                    for (var dependency : dependencies) {
                        parameters.add(dependency, result.get(dependency));
                    }

                    dependentPipeline.setupDependency(parameters);
                }

                if (pipeline instanceof IWithInput withInputPipeline) {
                    var dependencies = withInputPipeline.getClass().getAnnotation(Pipeline.class).inputDependencies();
                    var dependencyModels = new ArrayList<Cell<Model>>();

                    for (var dependency : dependencies) {
                        dependencyModels.add(modelCache.get(dependency));
                    }

                    withInputPipeline.setupInput(CellUtils.sequence(dependencyModels).map(models -> {
                        var doubleInputs = Tree.<String, CellSink<Double>>create();
                        var integerInputs = Tree.<String, CellSink<Integer>>create();

                        models.forEach(model -> {
                            doubleInputs.combine(model.doubleInputs());
                            integerInputs.combine(model.intInputs());
                        });

                        return new Model(doubleInputs, integerInputs);
                    }));
                }

                if(pipeline instanceof CellPipeline<?> cellPipeline)
                    result.put(pipelineClass, cellPipeline.define());
                else if(pipeline instanceof SynchronousPipeline<?> synchronousPipeline)
                    synchronousPipelines.put(pipelineClass, synchronousPipeline);

                return pipeline;
            }
        });

        var dependencyGraph = new DefaultDexecutor<>(config);

        for (var pipeline : toSetup) {
            var dependencies = pipeline.getClass().getAnnotation(Pipeline.class).dependencies();

            for (var dependency : dependencies) {
                dependencyGraph.addDependency(dependency, pipeline.getClass());
            }
        }

        dependencyGraph.execute(ExecutionConfig.NON_TERMINATING);

        return result;
    }
}
