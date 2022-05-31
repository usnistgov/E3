package gov.nist.e3.util.dependency;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

class Node<K> {
    private final K id;
    private final List<Node<K>> dependencies;

    public Node(K id, List<Node<K>> previousNodes) {
        this.id = id;
        this.dependencies = previousNodes;
    }

    public Set<K> get() {
        var result = new HashSet<K>();

        result.add(id);

        for (var node : dependencies) {
            result.addAll(node.get());
        }

        return result;
    }
}
