package gov.nist.eee.pipeline.sensitivity;

import gov.nist.eee.ComputeModel;
import net.jqwik.api.Example;
import nz.sodium.*;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;

class SensitivityPipelineTest {
    record Test(int x, int y, List<Integer> values) {
    }

    @Example
    void test() {
        var stream = new StreamSink<Test>();

        var inX = stream.map(Test::x).map(CellSink::new);
        var inY = stream.map(Test::y).map(CellSink::new);
        var inValues = stream.map(Test::values).hold(List.of());

        var ySink = inX.hold(new CellSink<>(0));
        var zSink = inY.hold(new CellSink<>(0));

        var y = Cell.switchC(ySink.map(c -> c.map(i -> i - 1)));
        var z = Cell.switchC(zSink.map(c -> c.map(i -> i + 2)));

        var res = y.lift(z, Integer::sum);

        //res.listen(System.out::println);

        AtomicInteger sum = new AtomicInteger();

        inValues.lift(ySink, (values, sink) -> {
            var result = new ArrayList<>();

            for (var value : values) {
                Transaction.runVoid(() -> {
                    sink.send(value);

                    Transaction.post(() -> {
                        System.out.println(res.sample());
                        sum.addAndGet(res.sample());
                    });
                });
            }

            Transaction.post(() -> System.out.println(sum.get()));

            return result;
        });

        Transaction.runVoid(() -> {
            stream.send(new Test(2, 3, List.of(5, 6, 7, 8, 9, 10)));
        });

        /*var sink = new StreamSink<List<Integer>>();

        var stream1 = sink.map(i -> {
            var size = i.size();

            var value = Operational.split(sink).map(j -> {
                System.out.println("Inside send " + j);
                Transaction.post(() -> x.send(j));
                return model.sample();
            }).accum(new ArrayList<Integer>(), (k, l) -> {
                l.add(k);
                return l;
            });

            return CellUtils.ignore(size - 1, Operational.updates(value));
        }).hold(new Stream<>());

        Cell.switchS(stream1).listen(System.out::println);

        sink.send(List.of(1, 2, 3));
        sink.send(List.of(4, 5, 6));
        sink.send(List.of(7, 8, 9, 10));*/
    }

  /*  @Test
    void getValues() {
        var result = SensitivityPipeline.getValues(SensitivityDiffType.GROSS, 10.0, 0.03);
    }*/

    @Example
    void parallelTest() {

/*        var stream = new StreamSink<Integer>();

        var models = stream.hold(10).map(x -> {
            var result = new ArrayList<CellSink<Integer>>();

            for(int i = 0; i < 4; i++ ){
                var c = new CellSink<>(i);
                c.map(y -> {
                    try {
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    System.out.println(Thread.currentThread() + " " + y);
                    return y;
                }).listen(j -> System.out.println(Thread.currentThread() + " " + j));

                result.add(new CellSink<>(i));
            }

            return result;
        });*/

        System.out.println("Creating threads");
        var executor = Executors.newFixedThreadPool(4);
        //var m = models.sample();
        var futures = new ArrayList<Future<?>>();
        for(var i = 0; i < 4; i++) {
            int finalI = i;
            executor.execute(() -> {
                System.out.println(Thread.currentThread().toString());
                var c2 = Transaction.run(() -> {
                    var c = new CellSink<>(finalI);
                    c.map(y -> {
                        try {
                            Thread.sleep(2000);
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        }
                        System.out.println(Thread.currentThread() + " " + y);
                        return y;
                    }).listen(j -> System.out.println(Thread.currentThread() + " " + j));
                    return c;
                });

                Transaction.runVoid(() -> {
                    c2.send(finalI);
                });
            });
           // futures.add(f);
        }

        try {
            Thread.sleep(4000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

/*        futures.stream().forEach(x -> {
            try {
                x.get();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (ExecutionException e) {
                throw new RuntimeException(e);
            }
        });*/

    }
}