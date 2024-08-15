package supplier;

import gov.nist.eee.tuple.Tuple2;
import net.jqwik.api.Arbitraries;
import net.jqwik.api.Arbitrary;
import net.jqwik.api.ArbitrarySupplier;

public class LessThanOrEqualSupplier implements ArbitrarySupplier<Tuple2<Integer, Integer>> {
    @Override
    public Arbitrary<Tuple2<Integer, Integer>> get() {
        return Arbitraries.integers().flatMap(x -> Arbitraries.integers().lessOrEqual(x).map(y -> new Tuple2<>(x, y)));
    }
}
