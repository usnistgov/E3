package supplier;

import gov.nist.eee.tuple.Tuple2;
import net.jqwik.api.Arbitraries;
import net.jqwik.api.Arbitrary;
import net.jqwik.api.ArbitrarySupplier;

public class GreaterThanSupplier implements ArbitrarySupplier<Tuple2<Integer, Integer>> {
    @Override
    public Arbitrary<Tuple2<Integer, Integer>> get() {
        return Arbitraries.integers()
                .between(Integer.MIN_VALUE + 1, Integer.MAX_VALUE)
                .flatMap(larger -> Arbitraries.integers()
                        .between(Integer.MIN_VALUE, larger - 1)
                        .map(smaller -> new Tuple2<>(larger, smaller))
                );
    }
}
