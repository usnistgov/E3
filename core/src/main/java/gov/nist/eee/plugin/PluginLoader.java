package gov.nist.eee.plugin;

import gov.nist.eee.config.Config;
import gov.nist.eee.fileutils.Watcher;
import gov.nist.eee.object.InputExtension;
import gov.nist.eee.output.IOutputMapper;
import gov.nist.eee.pipeline.*;
import gov.nist.eee.util.CellUtils;
import nz.sodium.Cell;
import nz.sodium.Tuple2;
import org.atteo.classindex.ClassIndex;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.lang.module.ModuleDescriptor;
import java.lang.module.ModuleFinder;
import java.lang.module.ModuleReference;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;

public class PluginLoader {
    private static final Logger logger = LoggerFactory.getLogger(PluginLoader.class);

    /**
     * The directory to load plugins from and watch for changes.
     */
    private final Cell<Path> pluginDirectory = Config.cConfigs
            .map(config -> (String) ((Map<String, Object>) config.get("core")).getOrDefault("pluginDirectory", "../plugins"))
            .map(Path::of);

    /**
     * Creates a new file watcher on the plugin directory and closes the previous one if necessary.
     */
    private final Cell<Watcher> cPluginWatcher = CellUtils.withCleanup(
            pluginDirectory.map(Watcher::new),
            Watcher::close
    );

    /**
     * Classloader for all the jars in the plugin directory. This is recreated on a file watcher event. All references
     * should be released so previous class loader gets garbage collected/
     */
    private final Cell<URLClassLoader> cClassLoader = Cell.switchC(
            pluginDirectory.map(dir -> Cell.switchS(cPluginWatcher.map(Watcher::sUpdated)).mapTo(dir).hold(dir))
    )
            .map(this::getJarURLs)
            .map(this::createUrlClassLoader);

    /**
     * A map of input extension classes to the annotations that describe them loaded from plugins.
     */
    public final Cell<Map<Class<?>, InputExtension>> cInputExtensions = cClassLoader.map(this::getInputExtensions);

    /**
     * A list of all pipelines that are loaded from the plugins.
     */
    public final Cell<List<IPipeline<?>>> cPipelines = cClassLoader.map(this::loadPipelines);

    /**
     * A list of output mappers loaded from the plugins.
     */
    public final Cell<Map<Class<? extends IOutputMapper>, IOutputMapper>> cOutputMappers = cClassLoader.map(this::loadOutputMappers);

    public PluginLoader() {
        // Debug log plugin directory whenever it changes
        pluginDirectory.listen(directory -> logger.debug("Watching plugin directory " + directory.toString()));
    }

    /**
     * Creates a new {@link URLClassLoader} that loads all the given URLs.
     *
     * @param urls The URLs of jars to load with the new class loader.
     * @return The new class loader containing the URLs.
     */
    private URLClassLoader createUrlClassLoader(final List<URL> urls) {
        return new URLClassLoader(urls.toArray(new URL[0]), PluginLoader.class.getClassLoader());
    }

    /**
     * Gets all the input extensions from the classes loaded by the given class loader.
     *
     * @param loader The class loader to get {@link InputExtension}s from.
     * @return A {@link HashMap} of classes to their {@link InputExtension} annotations.
     */
    private HashMap<Class<?>, InputExtension> getInputExtensions(final URLClassLoader loader) {
        var result = new HashMap<Class<?>, InputExtension>();

        for(var clazz : ClassIndex.getAnnotated(InputExtension.class, loader)) {
            result.put(clazz, clazz.getAnnotation(InputExtension.class));
        }

        return result;
    }

    /**
     * Get the URLs of all "*.jar" files in the plugin directory.
     *
     * @param pluginDirectory The directory to retrieve jar files from.
     * @return A list of all "*.jar" files found in the plugin directory.
     */
    private List<URL> getJarURLs(final Path pluginDirectory) {
        var result = new ArrayList<URL>();

        try(var jars = Files.newDirectoryStream(pluginDirectory, "*.jar")) {
            for(var jarPath : jars) {
                result.add(jarPath.toUri().toURL());
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return result;
    }

    /**
     * Loads all instances of the given class from the given class loader using {@link ServiceLoader}.
     *
     * @param loader The class loader to retrieve services from.
     * @param clazz The type of the service to load.
     * @return A list of classes that implement the service class.
     * @param <A> The service class type.
     */
    private <A> List<A> loadServices(final URLClassLoader loader, final Class<A> clazz) {
        return ServiceLoader.load(clazz, loader).stream().map(ServiceLoader.Provider::get).toList();
    }

    /**
     * Returns a list of classes that implement the {@link IPipeline} interface.
     *
     * @param loader The class loader to get the services from.
     * @return A list of classes from the class loader that implement {@link IPipeline}.
     */
    private List<IPipeline<?>> loadPipelines(final URLClassLoader loader) {
        logger.trace("Loading Pipelines from URL class loader");
        var result = new ArrayList<IPipeline<?>>();
        loadServices(loader, IPipeline.class).forEach(result::add);

        return result;
    }

    /**
     * Loads all output mappers that implement {@link OutputMapper} from the given class loader.
     *
     * @param loader The class loader to get the output mappers from.
     * @return A map of output mapper classes to their instance.
     */
    private Map<Class<? extends IOutputMapper>, IOutputMapper> loadOutputMappers(final URLClassLoader loader) {
        logger.trace("Loading Output Mappers");
        var services = loadServices(loader, IOutputMapper.class);

        logger.debug("Services " + services);

        return services.stream().collect(Collectors.toMap(IOutputMapper::getClass, x -> x));
    }
}
