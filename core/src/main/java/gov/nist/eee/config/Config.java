package gov.nist.eee.config;

import gov.nist.eee.fileutils.FileWatcher;
import nz.sodium.Cell;
import org.yaml.snakeyaml.Yaml;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

public class Config {
    //Path.of("../config.yml");              Path.of("./app/config.yml");
    private static final Path CONFIG_PATH = Path.of("./app/config.yml");
    private static final Yaml YAML = new Yaml();
    private static final FileWatcher WATCHER = new FileWatcher(CONFIG_PATH);


    public static Cell<Map<String, Object>> cConfigs = WATCHER.sCreated()
            .orElse(WATCHER.sModified())
            .mapTo(CONFIG_PATH)
            .hold(CONFIG_PATH)
            .map(p -> {
                try {
                    return YAML.load(Files.newBufferedReader(p));
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
}
