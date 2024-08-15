package supplier;

import net.jqwik.api.Arbitraries;
import net.jqwik.api.Arbitrary;
import net.jqwik.api.ArbitrarySupplier;
import net.jqwik.api.providers.TypeUsage;
import nz.sodium.Cell;
import nz.sodium.CellSink;

public class CellSupplier implements ArbitrarySupplier<Cell<?>> {
    @Override
    public Arbitrary<Cell<?>> supplyFor(TypeUsage targetType) {
        var typeArg = targetType.getTypeArgument(0);
        if (typeArg.getRawType() == CellSink.class)
            return new CellSinkSupplier().supplyFor(typeArg).map(Cell::new);

        return Arbitraries.defaultFor(targetType.getTypeArgument(0)).map(Cell::new);
    }
}