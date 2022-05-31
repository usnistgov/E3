package gov.nist.e3.objects.input;

import com.fasterxml.jackson.annotation.*;
import gov.nist.e3.tree.ToTree;
import gov.nist.e3.tree.Tree;
import gov.nist.e3.util.ToCell;
import nz.sodium.CellSink;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;
import java.util.Objects;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public final class Bcn implements ToTree<String, CellSink<? extends Number>>, ToCell<BcnCell> {
    @NotNull
    private final int id;

    @NotNull
    private final List<Integer> altIds;

    @NotNull
    private final BcnType type;

    @Nullable
    private final BcnSubType subType;

    @Nullable
    private final String name;

    @Nullable
    private final List<String> tags;

    private final int initialOccurrence;

    private final boolean real;

    @JsonProperty("invest")
    private boolean invest;

    @Nullable
    private final Integer life;

    private final boolean residualValue;

    private final boolean residualValueOnly;

    @Nullable
    private final RecurOptions recur;

    @Nullable
    private final Double quantityValue;

    private final double quantity;

    @Nullable
    private final VarRate quantityVarRate;

    @Nullable
    private final List<Double> quantityVarValue;

    @Nullable
    private final String quantityUnit;

    @JsonIgnore
    private transient BcnCell bcnCell;

    public Bcn() {
        id = 0;
        altIds = List.of();
        type = BcnType.COST;
        subType = BcnSubType.DIRECT;
        name = "";
        tags = List.of();
        initialOccurrence = 0;
        real = false;
        invest = false;
        life = 0;
        residualValue = false;
        residualValueOnly = false;
        recur = null;
        quantityValue = 0.0;
        quantity = 0.0;
        quantityVarRate = null;
        quantityVarValue = null;
        quantityUnit = "";
    }

    public Bcn(
            int id,
            List<Integer> altIds,
            BcnType type,
            BcnSubType subType,
            String name,
            List<String> tags,
            int initialOccurrence,
            boolean real,
            boolean invest,
            int life,
            boolean residualValue,
            boolean residualValueOnly,
            RecurOptions recur,
            double quantityValue,
            double quantity,
            VarRate quantityVarRate,
            List<Double> quantityVarValue,
            String quantityUnit
    ) {
        this.id = id;
        this.altIds = altIds;
        this.type = type;
        this.subType = subType;
        this.name = name;
        this.tags = tags;
        this.initialOccurrence = initialOccurrence;
        this.real = real;
        this.invest = invest;
        this.life = life;
        this.residualValue = residualValue;
        this.residualValueOnly = residualValueOnly;
        this.recur = recur;
        this.quantityValue = quantityValue;
        this.quantity = quantity;
        this.quantityVarRate = quantityVarRate;
        this.quantityVarValue = quantityVarValue;
        this.quantityUnit = quantityUnit;

        this.bcnCell = this.toCell();
    }

    @JsonIgnore
    public boolean isCost() {
        return type() == BcnType.COST;
    }

    @JsonIgnore
    public boolean isBenefit() {
        return type() == BcnType.BENEFIT;
    }

    @JsonIgnore
    public boolean isInvest() {
        return invest();
    }

    @JsonIgnore
    public boolean isNonInvest() {
        return !isInvest();
    }

    @JsonIgnore
    public boolean isDirect() {
        return subType() == BcnSubType.DIRECT;
    }

    @JsonIgnore
    public boolean isIndirect() {
        return subType() == BcnSubType.INDIRECT;
    }

    @JsonIgnore
    public boolean isExternality() {
        return subType() == BcnSubType.EXTERNALITY;
    }

    @Override
    public Tree<String, CellSink<? extends Number>> toTree() {
        var result = Tree.<String, CellSink<? extends Number>>create();

        result.add("initialOccurrence", cInitialOccurrence());
        result.add("life", cLife());

        if (recur != null)
            result.addTree("recur", recur.toTree());
        
        result.add("quantityValue", cQuantityValue());
        result.add("quantity", cQuantity());

        return result;
    }

    public int id() {
        return id;
    }

    public List<Integer> altIds() {
        return altIds;
    }

    public BcnType type() {
        return type;
    }

    public BcnSubType subType() {
        return subType;
    }

    public String name() {
        return name;
    }

    public List<String> tags() {
        return tags;
    }

    public int initialOccurrence() {
        return initialOccurrence;
    }

    public boolean real() {
        return real;
    }

    public boolean invest() {
        return invest;
    }

    public int life() {
        return life;
    }

    public boolean residualValue() {
        return residualValue;
    }

    public boolean residualValueOnly() {
        return residualValueOnly;
    }

    public RecurOptions recur() {
        return recur;
    }

    public double quantityValue() {
        return quantityValue;
    }

    public double quantity() {
        return quantity;
    }

    public VarRate quantityVarRate() {
        return quantityVarRate;
    }

    public List<Double> quantityVarValue() {
        return quantityVarValue;
    }

    public String quantityUnit() {
        return quantityUnit;
    }

    public void checkCell() {
        if (bcnCell == null)
            this.bcnCell = toCell();
    }

    public CellSink<Integer> cInitialOccurrence() {
        checkCell();
        return bcnCell.cInitialOccurrence();
    }

    public CellSink<Integer> cLife() {
        checkCell();
        return bcnCell.cLife();
    }

    public CellSink<Double> cQuantityValue() {
        checkCell();
        return bcnCell.cQuantityValue();
    }

    public CellSink<Double> cQuantity() {
        checkCell();
        return bcnCell.cQuantity();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;
        if (obj == null || obj.getClass() != this.getClass()) return false;
        var that = (Bcn) obj;
        return this.id == that.id &&
                this.altIds == that.altIds &&
                Objects.equals(this.type, that.type) &&
                Objects.equals(this.subType, that.subType) &&
                Objects.equals(this.name, that.name) &&
                Objects.equals(this.tags, that.tags) &&
                this.initialOccurrence == that.initialOccurrence &&
                this.real == that.real &&
                this.invest == that.invest &&
                this.life.equals(that.life) &&
                this.residualValue == that.residualValue &&
                this.residualValueOnly == that.residualValueOnly &&
                Objects.equals(this.recur, that.recur) &&
                Double.doubleToLongBits(this.quantityValue) == Double.doubleToLongBits(that.quantityValue) &&
                Double.doubleToLongBits(this.quantity) == Double.doubleToLongBits(that.quantity) &&
                Objects.equals(this.quantityVarRate, that.quantityVarRate) &&
                Objects.equals(this.quantityVarValue, that.quantityVarValue) &&
                Objects.equals(this.quantityUnit, that.quantityUnit);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, altIds, type, subType, name, tags, initialOccurrence, real, invest, life, residualValue, residualValueOnly, recur, quantityValue, quantity, quantityVarRate, quantityVarValue, quantityUnit);
    }

    @Override
    public String toString() {
        return "Bcn[" +
                "id=" + id + ", " +
                "altId=" + altIds + ", " +
                "type=" + type + ", " +
                "subType=" + subType + ", " +
                "name=" + name + ", " +
                "tag=" + tags + ", " +
                "initialOccurrence=" + initialOccurrence + ", " +
                "real=" + real + ", " +
                "invest=" + invest + ", " +
                "life=" + life + ", " +
                "residualValue=" + residualValue + ", " +
                "residualValueOnly=" + residualValueOnly + ", " +
                "recur=" + recur + ", " +
                "quantityValue=" + quantityValue + ", " +
                "quantity=" + quantity + ", " +
                "quantityVarRate=" + quantityVarRate + ", " +
                "quantityVarValue=" + quantityVarValue + ", " +
                "quantityUnit=" + quantityUnit + ']';
    }

    @Override
    public BcnCell toCell() {
        return new BcnCell(
                new CellSink<>(initialOccurrence),
                new CellSink<>(life),
                new CellSink<>(quantityValue),
                new CellSink<>(quantity)
        );
    }
}

