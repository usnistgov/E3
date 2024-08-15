package gov.nist.eee.object.tree;

/**
 * This is the base interface for the Tree algebraic data type.
 *
 * @param <K> The key type of the tree.
 * @param <V> The value type of the tree.
 */
public interface Tree<K, V> extends Iterable<V> {
    /**
     * Creates a new Tree instance with a root node that can be added on to.
     *
     * @param <K> The key type of the tree.
     * @param <V> The value type of the tree.
     * @return The root node of a new tree.
     */
    static <K, V> Tree<K, V> create() {
        return new Node<>();
    }

    /**
     * Adds the given subtree onto this tree at the specified tree.
     *
     * @param key The key to attach the subtree at.
     * @param other The subtree to attach to this tree.
     * @throws IllegalArgumentException if the specified key already exists withint the tree.
     */
    void addTree(K key, Tree<K, V> other);

    /**
     * Adds the given value onto this tree.
     *
     * @param path The key to add the value at.
     * @param value The value to add to the tree.
     * @throws IllegalArgumentException if the specified path already exists within the tree.
     */
    void add(K path, V value);

    /**
     * Adds the given value onto this tree at the given onto this tree at the specified path within the tree.
     *
     * @param path The path of keys to add the value at.
     * @param value The value to add to the tree.
     * @throws IllegalArgumentException if the specified path is  a value already exists at that path in the tree.
     */
    void add(K[] path, V value);

    /**
     * Gets the value at the specified path.
     *
     * @param path The path of the value within the tree.
     * @return The value at the specified path.
     * @throws IllegalArgumentException if the specified path does not exist within the tree.
     */
    V get(K[] path);

    /**
     * Combine all branches and leaves in this tree with another tree. Fails if the two trees have an overlapping
     * leaf.
     *
     * @param other the tree to combine with.
     */
    void combine(Tree<K, V> other);
}

