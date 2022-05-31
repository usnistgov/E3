package gov.nist.e3.compute;

import gov.nist.e3.objects.input.VarRate;
import gov.nist.e3.util.Util;
import nz.sodium.Cell;
import nz.sodium.Transaction;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public class ValuePipeline {
    public final Cell<List<Double>> cValues;

    public ValuePipeline(
            @NotNull Cell<@NotNull List<Double>> cQuantities,
            @NotNull Cell<Double> cValuePerQ,
            @Nullable List<Double> varValue,
            @Nullable VarRate varRate
    ) {
        this.cValues = define(cQuantities, cValuePerQ, varValue, varRate);
    }

    private Cell<List<Double>> define(
            @NotNull Cell<@NotNull List<Double>> cQuantities,
            @NotNull Cell<Double> cValuePerQ,
            @Nullable List<Double> varValue,
            @Nullable VarRate varRate
    ) {
        return Transaction.run(() -> {
          var useVarRateMap = Util.nonNull(varValue, varRate);

          if(useVarRateMap) {
              var cInflatedVarValue = cQuantities.map(
                      quantities -> Util.inflateVarValue(varValue, quantities.size())
              );

              return  cInflatedVarValue.map(values -> Util.mapWithVarRate(values, varRate))
                      .lift(cQuantities, Util::elementwiseMultiply)
                      .lift(cValuePerQ, Util::multiplier);
          } else {
              return cQuantities.lift(cValuePerQ, Util::multiplier);
          }
        });
    }
}
