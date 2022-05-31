package gov.nist.e3.objects.input;

import gov.nist.e3.tree.ToTree;
import gov.nist.e3.tree.Tree;
import nz.sodium.Cell;
import org.springframework.validation.annotation.Validated;

@Validated
public record Location(String address, String city, String state, String zip) implements ToTree<String, Cell<?>> {
    @Override
    public Tree<String, Cell<?>> toTree() {
        var result = Tree.<String, Cell<?>>create();

        result.add("address", new Cell<>(address()));
        result.add("city", new Cell<>(city()));
        result.add("state", new Cell<>(state()));
        result.add("zip", new Cell<>(zip()));

        return result;
    }
}
