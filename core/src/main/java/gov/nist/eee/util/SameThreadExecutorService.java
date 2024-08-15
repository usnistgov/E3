package gov.nist.eee.util;

import java.util.Collections;
import java.util.List;
import java.util.concurrent.AbstractExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Executes all submitted tasks directly in the same thread as the caller.
 */
public class SameThreadExecutorService extends AbstractExecutorService {

    //volatile because can be viewed by other threads
    private volatile boolean terminated;

    @Override
    public void shutdown() {
        terminated = true;
    }

    @Override
    public boolean isShutdown() {
        return terminated;
    }

    @Override
    public boolean isTerminated() {
        return terminated;
    }

    @Override
    public boolean awaitTermination(long theTimeout, TimeUnit theUnit) throws InterruptedException {
        shutdown(); // TODO ok to call shutdown? what if the client never called shutdown???
        return terminated;
    }

    @Override
    public List<Runnable> shutdownNow() {
        return Collections.emptyList();
    }

    @Override
    public void execute(Runnable theCommand) {
        theCommand.run();
    }
}