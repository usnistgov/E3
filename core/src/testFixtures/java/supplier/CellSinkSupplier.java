package supplier;

import net.jqwik.api.Arbitraries;
import net.jqwik.api.Arbitrary;
import net.jqwik.api.ArbitrarySupplier;
import net.jqwik.api.providers.TypeUsage;
import nz.sodium.Cell;
import nz.sodium.CellSink;

public class CellSinkSupplier implements ArbitrarySupplier<CellSink<?>> {
    @Override
    public Arbitrary<CellSink<?>> supplyFor(TypeUsage targetType) {
        var typeArg = targetType.getTypeArgument(0);
        if (typeArg.getRawType() == Cell.class)
            return new CellSupplier().supplyFor(typeArg).map(CellSink::new);

        return Arbitraries.defaultFor(targetType.getTypeArgument(0)).map(CellSink::new);
    }
}