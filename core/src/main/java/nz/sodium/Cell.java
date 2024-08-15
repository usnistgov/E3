package nz.sodium;

/**
 * Represents a value of type A that changes over time.
 */
public class Cell<A> {
    final Stream<A> str;
    A value;
    A valueUpdate;
    private Listener cleanup;
    Lazy<A> lazyInitValue;  // Used by LazyCell

    /**
     * A cell with a constant value.
     */
    public Cell(A value) {
        this.str = new Stream<>();
        this.value = value;
    }

    Cell(final Stream<A> str, A initValue) {
        this.str = str;
        this.value = initValue;
        Transaction.run(trans1 -> Cell.this.cleanup = str.listen(Node.NULL, trans1, (trans2, a) -> {
            if (Cell.this.valueUpdate == null) {
                trans2.last(() -> {
                    Cell.this.value = Cell.this.valueUpdate;
                    Cell.this.lazyInitValue = null;
                    Cell.this.valueUpdate = null;
                });
            }
            Cell.this.valueUpdate = a;
        }, false));
    }

    /**
     * @return The value including any updates that have happened in this transaction.
     */
    final A newValue() {
        return valueUpdate == null ? sampleNoTrans() : valueUpdate;
    }

    /**
     * Sample the cell's current value.
     * <p>
     * It may be used inside the functions passed to primitives that apply them to {@link Stream}s,
     * including {@link Stream#map(Lambda1)} in which case it is equivalent to snapshotting the cell,
     * {@link Stream#snapshot(Cell, Lambda2)}, {@link Stream#filter(Lambda1)} and
     * {@link Stream#merge(Stream, Lambda2)}.
     * It should generally be avoided in favour of {@link #listen(Handler)} so you don't
     * miss any updates, but in many circumstances it makes sense.
     */
    public final A sample() {
        return Transaction.apply(trans -> sampleNoTrans());
    }

    private static class LazySample<A> {
        LazySample(Cell<A> cell) {
            this.cell = cell;
        }

        Cell<A> cell;
        boolean hasValue;
        A value;
    }

    /**
     * A variant of {@link #sample()} that works with {@link CellLoop}s when they haven't been looped yet.
     * It should be used in any code that's general enough that it could be passed a {@link CellLoop}.
     *
     * @see Stream#holdLazy(Lazy) Stream.holdLazy()
     */
    public final Lazy<A> sampleLazy() {
        return Transaction.apply(this::sampleLazy);
    }

    final Lazy<A> sampleLazy(Transaction trans) {
        final LazySample<A> s = new LazySample<>(this);
        trans.last(() -> {
            s.value = this.valueUpdate != null ? this.valueUpdate : this.sampleNoTrans();
            s.hasValue = true;
            s.cell = null;
        });
        return new Lazy<>(() -> {
            if (s.hasValue)
                return s.value;
            else
                return s.cell.sample();
        });
    }

    A sampleNoTrans() {
        return value;
    }

    final Stream<A> updates() {
        return str;
    }

    final Stream<A> value(Transaction trans1) {
        final StreamWithSend<Unit> sSpark = new StreamWithSend<>();
        trans1.prioritized(sSpark.node, trans2 -> sSpark.send(trans2, Unit.UNIT));
        Stream<A> sInitial = sSpark.snapshot(this);
        return sInitial.merge(updates(), (left, right) -> right);
    }

    /**
     * Transform the cell's value according to the supplied function, so the returned Cell
     * always reflects the value of the function applied to the input Cell's value.
     *
     * @param f Function to apply to convert the values. It must be <em>referentially transparent</em>.
     */
    public final <B> Cell<B> map(final Lambda1<A, B> f) {
        return Transaction.apply(trans -> updates().map(f).holdLazy(trans, sampleLazy(trans).map(f)));
    }

    /**
     * Lift a binary function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     */
    public final <B, C> Cell<C> lift(Cell<B> b, final Lambda2<A, B, C> fn) {
        Lambda1<A, Lambda1<B, C>> ffa = aa -> (Lambda1<B, C>) bb -> fn.apply(aa, bb);
        Cell<Lambda1<B, C>> bf = this.map(ffa);
        return apply(bf, b);
    }

    /**
     * Lift a ternary function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     */
    public final <B, C, D> Cell<D> lift(Cell<B> b, Cell<C> c, final Lambda3<A, B, C, D> fn) {
        Lambda1<A, Lambda1<B, Lambda1<C, D>>> ffa = aa ->
                (Lambda1<B, Lambda1<C, D>>) bb ->
                        (Lambda1<C, D>) cc -> fn.apply(aa, bb, cc);
        Cell<Lambda1<B, Lambda1<C, D>>> bf = this.map(ffa);
        return apply(apply(bf, b), c);
    }

    /**
     * Lift a quaternary function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     */
    public final <B, C, D, E> Cell<E> lift(Cell<B> b, Cell<C> c, Cell<D> d, final Lambda4<A, B, C, D, E> fn) {
        Lambda1<A, Lambda1<B, Lambda1<C, Lambda1<D, E>>>> ffa = aa ->
                (Lambda1<B, Lambda1<C, Lambda1<D, E>>>) bb ->
                        (Lambda1<C, Lambda1<D, E>>) cc ->
                                (Lambda1<D, E>) dd -> fn.apply(aa, bb, cc, dd);
        Cell<Lambda1<B, Lambda1<C, Lambda1<D, E>>>> bf = this.map(ffa);
        return apply(apply(apply(bf, b), c), d);
    }

    /**
     * Lift a 5-argument function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     */
    public final <B, C, D, E, F> Cell<F> lift(Cell<B> b, Cell<C> c, Cell<D> d, Cell<E> e, final Lambda5<A, B, C, D, E, F> fn) {
        Lambda1<A, Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, F>>>>> ffa = new Lambda1<A, Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, F>>>>>() {
            public Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, F>>>> apply(final A aa) {
                return new Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, F>>>>() {
                    public Lambda1<C, Lambda1<D, Lambda1<E, F>>> apply(final B bb) {
                        return new Lambda1<C, Lambda1<D, Lambda1<E, F>>>() {
                            public Lambda1<D, Lambda1<E, F>> apply(final C cc) {
                                return new Lambda1<D, Lambda1<E, F>>() {
                                    public Lambda1<E, F> apply(final D dd) {
                                        return new Lambda1<E, F>() {
                                            public F apply(E ee) {
                                                return fn.apply(aa, bb, cc, dd, ee);
                                            }
                                        };
                                    }
                                };
                            }
                        };
                    }
                };
            }
        };
        Cell<Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, F>>>>> bf = this.map(ffa);
        return this.apply(apply(apply(apply(bf, b), c), d), e);
    }

    /**
     * Lift a 6-argument function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     */
    public final <B, C, D, E, F, G> Cell<G> lift(Cell<B> b, Cell<C> c, Cell<D> d, Cell<E> e, Cell<F> f, final Lambda6<A, B, C, D, E, F, G> fn) {
        Lambda1<A, Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>>>> ffa = new Lambda1<A, Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>>>>() {
            public Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>>> apply(final A aa) {
                return new Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>>>() {
                    public Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>> apply(final B bb) {
                        return new Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>>() {
                            public Lambda1<D, Lambda1<E, Lambda1<F, G>>> apply(final C cc) {
                                return new Lambda1<D, Lambda1<E, Lambda1<F, G>>>() {
                                    public Lambda1<E, Lambda1<F, G>> apply(final D dd) {
                                        return new Lambda1<E, Lambda1<F, G>>() {
                                            public Lambda1<F, G> apply(final E ee) {
                                                return new Lambda1<F, G>() {
                                                    public G apply(final F ff) {
                                                        return fn.apply(aa, bb, cc, dd, ee, ff);
                                                    }
                                                };
                                            }
                                        };
                                    }
                                };
                            }
                        };
                    }
                };
            }
        };
        Cell<Lambda1<B, Lambda1<C, Lambda1<D, Lambda1<E, Lambda1<F, G>>>>>> bf = this.map(ffa);
        return this.apply(apply(apply(apply(apply(bf, b), c), d), e), f);
    }

    /**
     * Apply a value inside a cell to a function inside a cell. This is the
     * primitive for all function lifting.
     */
    public static <A, B> Cell<B> apply(final Cell<Lambda1<A, B>> bf, final Cell<A> ba) {
        return Transaction.apply(trans0 -> {
            final StreamWithSend<B> out = new StreamWithSend<>();

            class ApplyHandler implements Handler<Transaction> {
                ApplyHandler() {
                }

                Lambda1<A, B> f = null;
                boolean f_present = false;
                A a = null;
                boolean a_present = false;

                boolean pumping = false;

                @Override
                public void run(Transaction trans1) {
                    if (pumping)
                        return;

                    pumping = true;
                    trans1.prioritized(out.node, trans2 -> {
                        var x = f_present ? f : bf.sampleNoTrans();
                        var y = a_present ? a : ba.sampleNoTrans();

                        out.send(trans2, x.apply(y));
                        pumping = false;
                    });
                }
            }

            Node out_target = out.node;
            final Node in_target = new Node(0);
            Node.Target[] node_target_ = new Node.Target[1];
            in_target.linkTo(null, out_target, node_target_);
            final Node.Target node_target = node_target_[0];
            final ApplyHandler h = new ApplyHandler();
            Listener l1 = Operational.updates(bf).listen_(in_target, (trans1, f) -> {
                h.f = f;
                h.f_present = true;
                h.run(trans1);
            });
            Listener l2 = Operational.updates(ba).listen_(in_target, (trans1, a) -> {
                h.a = a;
                h.a_present = true;
                h.run(trans1);
            });
            return out.lastFiringOnly(trans0).unsafeAddCleanup(l1).unsafeAddCleanup(l2).unsafeAddCleanup(
                    new Listener() {
                        public void unlisten() {
                            in_target.unlinkTo(node_target);
                        }
                    }
            ).holdLazy(new Lazy<>(() -> bf.sampleNoTrans().apply(ba.sampleNoTrans())));
        });
    }

    /**
     * Unwrap a cell inside another cell to give a time-varying cell implementation.
     */
    public static <A> Cell<A> switchC(final Cell<Cell<A>> bba) {
        return Transaction.apply(trans0 -> {
            Lazy<A> za = bba.sampleLazy().map(Cell::sample);
            final StreamWithSend<A> out = new StreamWithSend<>();
            TransactionHandler<Cell<A>> h = new TransactionHandler<>() {
                private Listener currentListener;

                @Override
                public void run(Transaction trans2, Cell<A> ba) {
                    // Note: If any switch takes place during a transaction, then the
                    // lastFiringOnly() below will always cause a sample to be fetched
                    // from the one we just switched to. So anything from the old input cell
                    // that might have happened during this transaction will be suppressed.
                    if (currentListener != null)
                        currentListener.unlisten();
                    currentListener = ba.value(trans2).listen(out.node, trans2, out::send, false);
                }

                @Override
                protected void finalize() throws Throwable {
                    if (currentListener != null)
                        currentListener.unlisten();
                }
            };
            Listener l1 = bba.value(trans0).listen_(out.node, h);
            return out.lastFiringOnly(trans0).unsafeAddCleanup(l1).holdLazy(za);
        });
    }

    /**
     * Unwrap a stream inside a cell to give a time-varying stream implementation.
     */
    public static <A> Stream<A> switchS(final Cell<Stream<A>> bea) {
        return Transaction.apply(trans -> switchS(trans, bea));
    }

    private static <A> Stream<A> switchS(final Transaction trans1, final Cell<Stream<A>> bea) {
        final StreamWithSend<A> out = new StreamWithSend<>();
        final TransactionHandler<A> h2 = out::send;
        TransactionHandler<Stream<A>> h1 = new TransactionHandler<>() {
            private Listener currentListener = bea.sampleNoTrans().listen(out.node, trans1, h2, false);

            @Override
            public void run(final Transaction trans2, final Stream<A> ea) {
                trans2.last(() -> {
                    if (currentListener != null)
                        currentListener.unlisten();
                    currentListener = ea.listen(out.node, trans2, h2, true);
                });
            }

            @Override
            protected void finalize() throws Throwable {
                if (currentListener != null)
                    currentListener.unlisten();
            }
        };
        Listener l1 = bea.updates().listen(out.node, trans1, h1, false);
        return out.unsafeAddCleanup(l1);
    }

    @Override
    protected void finalize() throws Throwable {
        if (cleanup != null)
            cleanup.unlisten();
    }

    /**
     * Listen for updates to the value of this cell. This is the observer pattern. The
     * returned {@link Listener} has a {@link Listener#unlisten()} method to cause the
     * listener to be removed. This is an OPERATIONAL mechanism is for interfacing between
     * the world of I/O and for FRP.
     *
     * @param action The handler to execute when there's a new value.
     *               You should make no assumptions about what thread you are called on, and the
     *               handler should not block. You are not allowed to use {@link CellSink#send(Object)}
     *               or {@link StreamSink#send(Object)} in the handler.
     *               An exception will be thrown, because you are not meant to use this to create
     *               your own primitives.
     */
    public final Listener listen(final Handler<A> action) {
        return Transaction.apply(trans -> value(trans).listen(action));
    }

    /**
     * A variant of {@link #listen(Handler)} that will deregister the listener automatically
     * if the listener is garbage collected. With {@link #listen(Handler)}, the listener is
     * only deregistered if {@link Listener#unlisten()} is called explicitly.
     */
    public final Listener listenWeak(final Handler<A> action) {
        return Transaction.apply(trans -> value(trans).listenWeak(action));
    }

    /**
     * Lift a binary function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     * @deprecated As of release 1.1.0, replaced by {@link #lift(Cell, Lambda2)}
     */
    @Deprecated
    public static final <A, B, C> Cell<C> lift(final Lambda2<A, B, C> fn, Cell<A> a, Cell<B> b) {
        return a.lift(b, fn);
    }

    /**
     * Lift a ternary function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     * @deprecated As of release 1.1.0, replaced by {@link #lift(Cell, Cell, Lambda3)}
     */
    @Deprecated
    public static final <A, B, C, D> Cell<D> lift(final Lambda3<A, B, C, D> fn, Cell<A> a, Cell<B> b, Cell<C> c) {
        return a.lift(b, c, fn);
    }

    /**
     * Lift a quaternary function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     * @deprecated As of release 1.1.0, replaced by {@link #lift(Cell, Cell, Cell, Lambda4)}
     */
    @Deprecated
    public static final <A, B, C, D, E> Cell<E> lift(final Lambda4<A, B, C, D, E> fn, Cell<A> a, Cell<B> b, Cell<C> c, Cell<D> d) {
        return a.lift(b, c, d, fn);
    }

    /**
     * Lift a 5-argument function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     * @deprecated As of release 1.1.0, replaced by {@link #lift(Cell, Cell, Cell, Cell, Lambda5)}
     */
    @Deprecated
    public static final <A, B, C, D, E, F> Cell<F> lift(final Lambda5<A, B, C, D, E, F> fn, Cell<A> a, Cell<B> b, Cell<C> c, Cell<D> d, Cell<E> e) {
        return a.lift(b, c, d, e, fn);
    }

    /**
     * Lift a 6-argument function into cells, so the returned Cell always reflects the specified
     * function applied to the input cells' values.
     *
     * @param fn Function to apply. It must be <em>referentially transparent</em>.
     * @deprecated As of release 1.1.0, replaced by {@link #lift(Cell, Cell, Cell, Cell, Cell, Lambda6)}
     */
    @Deprecated
    public static final <A, B, C, D, E, F, G> Cell<G> lift(final Lambda6<A, B, C, D, E, F, G> fn, Cell<A> a, Cell<B> b, Cell<C> c, Cell<D> d, Cell<E> e, Cell<F> f) {
        return a.lift(b, c, d, e, f, fn);
    }
}
