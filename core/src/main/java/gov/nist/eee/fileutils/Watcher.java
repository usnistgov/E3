package gov.nist.eee.fileutils;

import nz.sodium.Stream;
import nz.sodium.StreamSink;
import nz.sodium.Unit;

import java.io.IOException;
import java.nio.file.*;
import java.util.concurrent.TimeUnit;

import static java.nio.file.StandardWatchEventKinds.*;

public class Watcher implements AutoCloseable {
    private static long WAIT_TIME = 5;

    private WatchService service;
    private boolean shouldClose;

    private final StreamSink<WatchEvent<?>> sWatchEvent = new StreamSink<>();
    protected Stream<Path> sModified = sWatchEvent
            .filter(e -> e.kind().name().equals("ENTRY_MODIFY"))
            .map(e -> (Path) e.context());
    protected Stream<Path> sCreated = sWatchEvent
            .filter(e -> e.kind().name().equals("ENTRY_CREATE"))
            .map(e -> (Path) e.context());
    protected Stream<Path> sDeleted = sWatchEvent
            .filter(e -> e.kind().name().equals("ENTRY_DELETE"))
            .map(e -> (Path) e.context());

    protected Stream<Unit> sUpdated = sWatchEvent.mapTo(Unit.UNIT);

    public Watcher(final Path path) {
        try {
            service = FileSystems.getDefault().newWatchService();
            path.register(service, ENTRY_CREATE, ENTRY_MODIFY, ENTRY_DELETE);
        } catch (IOException e) {
            e.printStackTrace();
        }

        new Thread(this::callback).start();
        Runtime.getRuntime().addShutdownHook(new Thread(() -> shouldClose = true));
    }

    private void callback() {
        try {
            WatchKey key;
            while (!shouldClose) {
                key = service.poll(WAIT_TIME, TimeUnit.SECONDS);

                if(key != null) {
                    key.pollEvents().forEach(sWatchEvent::send);
                    key.reset();
                }
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public Stream<Path> sModified() {
        return sModified;
    }

    public Stream<Path> sCreated() {
        return sCreated;
    }

    public Stream<Path> sDeleted() {
        return sDeleted;
    }

    public Stream<Unit> sUpdated() {
        return sUpdated;
    }

    @Override
    public void close() {
        this.shouldClose = true;
    }
}
