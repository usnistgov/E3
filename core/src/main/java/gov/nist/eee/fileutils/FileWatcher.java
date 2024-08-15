package gov.nist.eee.fileutils;

import nz.sodium.Stream;

import java.nio.file.Files;
import java.nio.file.Path;

public class FileWatcher extends Watcher {
    private final Path path;

    public FileWatcher(final Path path) {
        super(path.getParent());

        if (!Files.isRegularFile(path))
            throw new IllegalArgumentException("Can only create file watcher on file. Given: " + path);

        this.path = path.getFileName();
    }

    private boolean equalsPath(final Path path) {
        return this.path.equals(path);
    }

    @Override
    public Stream<Path> sModified() {
        return this.sModified.filter(this::equalsPath);
    }

    @Override
    public Stream<Path> sCreated() {
        return this.sCreated.filter(this::equalsPath);
    }

    @Override
    public Stream<Path> sDeleted() {
        return this.sDeleted.filter(this::equalsPath);
    }
}
