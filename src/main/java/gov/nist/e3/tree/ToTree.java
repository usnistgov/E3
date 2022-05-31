package gov.nist.e3.tree;

/**
 * Implementers of this interface must implement a method that returns a tree, most likely a reflection of the
 * object's values.
 *
 * @param <K> The key type of the Tree.
 * @param <V> The value type of the Tree.
 */
public interface ToTree<K, V> {
    /**
     * Converts this object into a tree.
     *
     * @return A tree representation of this object.
     */
    Tree<K, V> toTree();
}
