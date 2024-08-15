package gov.nist.eee.object.tree;

import java.util.Iterator;

/**
 * Part of the Tree ADT that represents a leaf of the tree. Contains a value of type V.
 *
 * @param <K> The key type of the tree.
 * @param <V> The value type of the tree.
 */
public class Leaf<K, V> implements Tree<K, V> {
    protected final V value;

    public Leaf(V value) {
        this.value = value;
    }

    @Override
    public void addTree(K key, Tree<K, V> other) {
        throw new IllegalStateException("Cannot add tree to leaf");
    }

    @Override
    public void add(K path, V value) {
        throw new IllegalStateException("Cannot add value to leaf");
    }

    @Override
    public void add(K[] path, V value) {
        throw new IllegalStateException("Cannot add value to leaf");
    }

    @Override
    public V get(K[] path) {
        return value;
    }

    @Override
    public String toString() {
        if(value == null)
            return "null";

        return value.toString();
    }

    @Override
    public Iterator<V> iterator() {
        return new Iterator<>() {
            private boolean gave = false;

            @Override
            public boolean hasNext() {
                return !gave;
            }

            @Override
            public V next() {
                gave = true;
                return value;
            }
        };
    }

    @Override
    public void combine(Tree<K, V> other) {
        throw new IllegalStateException("Cannot combine a leaf value");
    }
}