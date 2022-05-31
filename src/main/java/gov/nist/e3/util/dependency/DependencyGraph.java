package gov.nist.e3.util.dependency;

import org.jetbrains.annotations.Nullable;

import java.util.*;

public class DependencyGraph<K> {
    private final Map<K, Node<K>> nodes = new HashMap<>();

    public void add(K id) {
        add(id, List.of());
    }

    public void add(K id, List<K> dependencies) {
        if(nodes.containsKey(id))
            throw new IllegalArgumentException("Node with id " + id + " already exists in dependency graph.");

        dependencies.stream()
                .map(nodes::containsKey)
                .reduce(Boolean::logicalAnd)
                .ifPresent(hasAllDependencies -> {
                    if(Boolean.FALSE.equals(hasAllDependencies))
                        throw new IllegalArgumentException("Graph does not contain correct dependencies.");
                });

        var dependencyNodes = new ArrayList<Node<K>>();

        for (var entry : nodes.entrySet()) {
            if (dependencies.contains(entry.getKey())) {
                dependencyNodes.add(entry.getValue());
            }
        }

        nodes.put(id, new Node<>(id, dependencyNodes));
    }

    public Set<K> get(K id) {
        return nodes.get(id).get();
    }

    public Set<K> getAll(@Nullable Collection<K> dependencies) {
        if(dependencies == null)
            return Set.of();

        var set = new HashSet<K>();

        for(var id : dependencies) {
            set.addAll(nodes.get(id).get());
        }

        return set;
    }

    @Override
    public String toString() {
        return nodes.toString();
    }
}

