package gov.nist.e3.objects.input;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import gov.nist.e3.tree.ToTree;
import gov.nist.e3.tree.Tree;
import gov.nist.e3.util.ToCell;
import nz.sodium.CellSink;

import java.util.List;
import java.util.Objects;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public final class RecurOptions implements ToTree<String, CellSink<? extends Number>>, ToCell<RecurOptionCell> {
    private final int interval;
    private final VarRate varRate;
    private final List<Double> varValue;
    private final int end;

    private transient RecurOptionCell recurOptionCell;

    public RecurOptions() {
        interval = 0;
        varRate = null;
        varValue = null;
        end = -1;

        this.recurOptionCell = null;
    }

    public RecurOptions(int interval, VarRate varRate, List<Double> varValue, int end) {
        this.interval = interval;
        this.varRate = varRate;
        this.varValue = varValue;
        this.end = end;

        this.recurOptionCell = toCell();
    }

    @Override
    public Tree<String, CellSink<? extends Number>> toTree() {
        var result = Tree.<String, CellSink<? extends Number>>create();

        result.add("interval", cInterval());
        result.add("end", cEnd());

        return result;
    }

    public int interval() {
        return interval;
    }

    public VarRate varRate() {
        return varRate;
    }

    public List<Double> varValue() {
        return varValue;
    }

    public int end() {
        return end;
    }

    private void checkCell() {
        if(this.recurOptionCell == null)
            this.recurOptionCell = toCell();
    }

    public CellSink<Integer> cInterval() {
        checkCell();
        return recurOptionCell.cInterval();
    }

    public CellSink<Integer> cEnd() {
        checkCell();
        return recurOptionCell.cEnd();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) return true;
        if (obj == null || obj.getClass() != this.getClass()) return false;
        var that = (RecurOptions) obj;
        return this.interval == that.interval &&
                Objects.equals(this.varRate, that.varRate) &&
                Objects.equals(this.varValue, that.varValue) &&
                this.end == that.end;
    }

    @Override
    public int hashCode() {
        return Objects.hash(interval, varRate, varValue, end);
    }

    @Override
    public String toString() {
        return "RecurOptions[" +
                "interval=" + interval + ", " +
                "varRate=" + varRate + ", " +
                "varValue=" + varValue + ", " +
                "end=" + end + ']';
    }

    @Override
    public RecurOptionCell toCell() {
        return new RecurOptionCell(
                new CellSink<>(interval()),
                new CellSink<>(end())
        );
    }
}
