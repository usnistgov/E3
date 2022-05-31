package gov.nist.e3.stream;

import nz.sodium.StreamSink;

import java.util.Random;

public class RandomStream extends StreamSink<Integer> {
    private final Random random;

    public RandomStream() {
        super();

        random = new Random();
    }

    public RandomStream(long seed) {
        super();

        random = new Random(seed);
    }

    public void next() {
        this.send(random.nextInt());
    }

    public void next(int amount) {
        random.ints(amount).forEach(this::send);
    }
}
