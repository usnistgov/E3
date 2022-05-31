package gov.nist.e3.tree;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * Part of the Tree ADT that represents a non-leaf node within the tree.
 *
 * @param <K> The key type of the tree.
 * @param <V> The value type of the tree.
 */
public class Node<K, V> implements Tree<K, V> {
    /**
     * The list of subtrees connected to this node.
     */
    protected final Map<K, Tree<K, V>> branches = new HashMap<>();

    @Override
    public void addTree(K key, Tree<K, V> other) {
        if (branches.containsKey(key))
            throw new IllegalArgumentException("Cannot add already existing node");

        branches.put(key, other);
    }

    @Override
    public void add(K path, V value) {
        if (branches.containsKey(path))
            throw new IllegalArgumentException("Value " + value + " is already in the tree");

        branches.put(path, new Leaf<>(value));
    }

    @Override
    public void add(K[] path, V value) {
        if (path.length == 1) {
            add(path[0], value);
        } else {
            var tree = branches.computeIfAbsent(path[0], k -> new Node<>());

            if (tree instanceof Node<K, V> node)
                node.add(Arrays.copyOfRange(path, 1, path.length), value);
            else
                throw new IllegalArgumentException("Value already exists at this path");
        }
    }

    @Override
    public V get(K[] path) {
        var result = branches.get(path[0]);

        if (result instanceof Node<K, V> node)
            return node.get(Arrays.copyOfRange(path, 1, path.length));
        else if (result instanceof Leaf<K, V> leaf)
            return leaf.value;

        throw new IllegalArgumentException("Path does not exist in tree");
    }

    @Override
    public String toString() {
        var builder = new StringBuilder();

        var entries = branches.entrySet();
        for (var iterator = entries.iterator(); iterator.hasNext(); ) {
            var branch = iterator.next();

            if (iterator.hasNext())
                builder.append('├');
            else
                builder.append('└');

            if (branch.getValue() instanceof Leaf<K, V> leaf) {
                builder.append(branch.getKey());
                builder.append(": ");
                builder.append(leaf);
                builder.append('\n');
            } else if (branch.getValue() instanceof Node<K, V> node) {
                var nodeString = node.toString();

                builder.append(branch.getKey());
                builder.append('\n');

                for (var token : nodeString.split("\\n")) {
                    if (iterator.hasNext())
                        builder.append('│');
                    else
                        builder.append(' ');
                    builder.append(token);
                    builder.append('\n');
                }

            }
        }

        return builder.toString();
    }

    @Override
    public Iterator<V> iterator() {
        var branchIterator = this.branches.values().iterator();


        return new Iterator<>() {
            Iterator<V> currentIterator = branchIterator.next().iterator();

            @Override
            public boolean hasNext() {
                return currentIterator.hasNext() || branchIterator.hasNext();
            }

            @Override
            public V next() {
                var result = currentIterator.next();

                if(!currentIterator.hasNext() && branchIterator.hasNext())
                    currentIterator = branchIterator.next().iterator();

                return result;
            }
        };
    }
}