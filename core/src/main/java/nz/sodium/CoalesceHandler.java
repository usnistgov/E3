package nz.sodium;

class CoalesceHandler<A> implements TransactionHandler<A> {
    public CoalesceHandler(Lambda2<A, A, A> f, StreamWithSend<A> out) {
        this.f = f;
        this.out = out;
    }

    private final Lambda2<A, A, A> f;
    private final StreamWithSend<A> out;
    private boolean accumValid = false;
    private A accum;

    @Override
    public void run(Transaction trans1, A a) {
        if (accumValid)
            accum = f.apply(accum, a);
        else {
            final CoalesceHandler<A> thiz = this;
            trans1.prioritized(out.node, trans2 -> {
                out.send(trans2, thiz.accum);
                thiz.accumValid = false;
                thiz.accum = null;
            });
            accum = a;
            accumValid = true;
        }
    }
}
