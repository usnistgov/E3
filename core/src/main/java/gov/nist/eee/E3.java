package gov.nist.eee;

import com.github.dexecutor.core.DefaultDexecutor;
import com.github.dexecutor.core.DexecutorConfig;
import com.github.dexecutor.core.ExecutionConfig;
import com.github.dexecutor.core.graph.LevelOrderTraversar;
import com.github.dexecutor.core.graph.StringTraversarAction;
import com.github.dexecutor.core.task.Task;
import gov.nist.eee.object.InputExtension;
import gov.nist.eee.object.Model;
import gov.nist.eee.object.input.Analysis;
import gov.nist.eee.object.input.Input;
import gov.nist.eee.object.tree.Tree;
import gov.nist.eee.output.*;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.plugin.PluginLoader;
import gov.nist.eee.util.CellUtils;
import gov.nist.eee.util.Result;
import gov.nist.eee.util.SameThreadExecutorService;
import gov.nist.eee.util.Util;
import nz.sodium.*;
import org.atteo.classindex.ClassIndex;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;
import java.util.stream.Collectors;

public class E3 {
    private static final Logger logger = LoggerFactory.getLogger(E3.class);

    private final PluginLoader plugins;
    private final StreamSink<Input> sInput = new StreamSink<>();
    private final Cell<Map<Class<? extends IOutputMapper>, IOutputMapper>> cOutputMappers;
    private final CellSink<State> cState = new CellSink<>(State.INIT);
    public final Cell<Map<Class<?>, InputExtension>> cInputExtensions;
    private Cell<Map<String, Object>> cOutputs;
    private final Map<Class<?>, SynchronousPipeline<?>> synchronousPipelines = new HashMap<>();
    private Cell<List<String>> cRequestedOutputs;

    {
        plugins = Transaction.run(PluginLoader::new);
    }

    public E3() {
        logger.trace("Initializing E3");

        // Get plugin output mappers and add default mappers
        cOutputMappers = plugins.cOutputMappers.map(E3::addDefaultOutputMappers);

        cOutputMappers.listen(System.out::println);

        Transaction.runVoid(this::initializationTransaction);

        cInputExtensions = plugins.cInputExtensions;

        cState.send(State.OUTPUT);
    }

    private static Map<Class<? extends IOutputMapper>, IOutputMapper> addDefaultOutputMappers(
            final Map<Class<? extends IOutputMapper>, IOutputMapper> mappers
    ) {
        mappers.put(CoreMapper.class, new CoreMapper());
        mappers.put(ResultOutputMapper.class, new ResultOutputMapper());
        mappers.put(ResultListMapper.class, new ResultListMapper());
        mappers.put(ResultNonSequenceOutputMapper.class, new ResultNonSequenceOutputMapper());
        return mappers;
    }

    private static Map<String, Cell<Object>> createPipelineOutputs(
            final Map<Class<?>, Cell<?>> definitions,
            final Map<Class<? extends IOutputMapper>, IOutputMapper> outputs
    ) {
        logger.debug("definitions " + definitions.toString());
        logger.debug("output map" + outputs.toString());

        return definitions.entrySet().stream().collect(Collectors.toMap(entry -> {
            logger.debug("entry " + entry);
            return entry.getKey().getAnnotation(Pipeline.class).name();
        }, entry -> getOutputMapper(entry, outputs)));
    }

    private void initializationTransaction() {
        Cell<Map<Class<?>, Cell<?>>> definitions = plugins.cPipelines.map(this::setup);

        var pipelineOutputs = definitions.lift(cOutputMappers, E3::createPipelineOutputs);

        // Get requested outputs from analysis object
        cRequestedOutputs = sInput.map(Input::analysis).map(Analysis::outputObjects).hold(List.of());

        cOutputs = Cell.switchC(pipelineOutputs.map(CellUtils::sequenceMap))
                .lift(cRequestedOutputs, (outputs, requested) ->
                        Util.<String, String, Object>toMap(x -> x, outputs::get).apply(requested)
                );

        //CellUtils.gate(cOutputs, cState.map(s -> s.equals(State.OUTPUT)))
        //        .listen(output -> listeners.forEach(consumer -> consumer.accept(output)));
    }

    @NotNull
    private static Cell<Object> getOutputMapper(Map.Entry<Class<?>, Cell<?>> entry, Map<Class<? extends IOutputMapper>, IOutputMapper> outputMap) {
        var sample = entry.getValue();
        var annotation = entry.getKey().getAnnotation(OutputMapper.class);

        if (annotation == null) return (Cell<Object>) sample;

        return outputMap.get(annotation.value()).outputMapper(sample);
    }

    public Map<Class<?>, Cell<?>> setup(List<IPipeline<?>> toSetup) {
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

    public Map<String, Object> analyze(final Input input) {
        logger.trace("Starting new calculation for input " + input.toString());

        // Update model
        sInput.send(input);

        // Setup variables and sample cells
        var result = new HashMap<String, Object>();
        var outputMappers = cOutputMappers.sample();
        var requestedOutputs = cRequestedOutputs.sample();

        // Sample regular outputs
        var outputs = cOutputs.sample();
        result.putAll(outputs);

        // Run synchronous analysis with
        logger.debug("Running synchronous pipelines");
        logger.debug("{}", synchronousPipelines);
        logger.debug("{}", requestedOutputs);
        logger.debug("{}", outputMappers);

        for(var entry: synchronousPipelines.entrySet()) {
            var clazz = entry.getKey();
            var pipeline = entry.getValue();
            var name = clazz.getAnnotation(Pipeline.class).name();

            if(!requestedOutputs.contains(name))
                continue;

            //var mapperClazz = clazz.getAnnotation(OutputMapper.class).value();
            //var mapper = outputMappers.get(mapperClazz);
            //var pipelineResult = mapper.outputMapper(pipeline.run());

            var pipelineResult = pipeline.run();
            if(pipelineResult instanceof Result.Success<?,?> success) {
                result.put(name, success.value());
            }

            //result.put(name, pipelineResult);
        }

        return result;
    }

    public InputStream getValidationSchema() {
        return E3.class.getResourceAsStream("/e3-request-schema.json");
    }
}