package gov.nist.eee.integration;

import gov.nist.eee.E3;
import gov.nist.eee.object.input.*;
import nz.sodium.Cell;
import nz.sodium.CellSink;
import nz.sodium.Handler;
import nz.sodium.Transaction;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.util.List;

class E3Test {
    //static E3 e3;

    @BeforeAll
    static void setup() {
        //System.out.println(System.getProperty("user.dir"));
        //e3 = new E3();
    }

    @Test
    void Test3() {
        System.out.println("-----Test 3-----");

        var a = new CellSink<>(new Cell<>(10));
        var b = new CellSink<>(new Cell<>(11));
        var combined = a.lift(b, (i, j) -> {
            System.out.println("inside lift1 " + i + " " + j);

            return i.lift(j, (k, l) -> {
                System.out.println("Inside lift2 " + k + " " + l);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                return k + l;
            });
        });

        var listener = Cell.switchC(combined).listen(System.out::println);

        var now = System.currentTimeMillis();
        Transaction.runVoid(() -> {
            System.out.println("Sending a");
            a.send(new Cell<>(1));
            System.out.println("Sending b");
            b.send(new Cell<>(2));
            System.out.println("done sending");
        });
        System.out.println(System.currentTimeMillis() - now);

        Transaction.runVoid(() -> {
            System.out.println("Sending a");
            a.send(new Cell<>(1));
            System.out.println("Sending b");
            b.send(new Cell<>(2));
            System.out.println("done sending");
        });

        listener.unlisten();
    }

    @Test
    void Test4() {
        System.out.println("-----Test 4-----");

        var a = new CellSink<>(new Cell<>(10));
        var b = new CellSink<>(new Cell<>(11));
        var combined = a.lift(b, (i, j) -> {
            System.out.println("inside lift1 " + i + " " + j);

            return Cell.switchC(i.map((k) -> {
                System.out.println("Inside lift2");
                return j.map((l) -> {
                    System.out.println("Inside lift3");
                    return k + l;
                });
            }));
        });

        var listener = Cell.switchC(combined).listen(System.out::println);

        var now = System.currentTimeMillis();
        Transaction.runVoid(() -> {
            System.out.println("Sending a");
            a.send(new Cell<>(1));
            System.out.println("Sending b");
            b.send(new Cell<>(2));
            System.out.println("done sending");
        });
        System.out.println(System.currentTimeMillis() - now);

        listener.unlisten();
    }

    /*@Test
    void testHandbook135() {
        var input = new Input(
                new Analysis(
                        AnalysisType.LCCA,
                        ProjectType.BUILDING,
                        List.of("measure"),
                        20,
                        TimestepValue.YEAR,
                        TimestepComp.END_OF_YEAR,
                        true,
                        null,
                        0.03,
                        null,
                        0.023,
                        0.03,
                        0.03,
                        null,
                        null,
                        null,
                        2,
                        0
                ),
                List.of(
                        new Bcn(
                                0,
                                List.of(0),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "HVAC System Conventional",
                                List.of("Initial Investment"),
                                0,
                                true,
                                true,
                                20,
                                false,
                                false,
                                null,
                                103000.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                1,
                                List.of(0),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Fan Replacement",
                                List.of("Replacement Costs"),
                                12,
                                true,
                                true,
                                null,
                                false,
                                false,
                                null,
                                12000.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                2,
                                List.of(0),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Electricity",
                                List.of("Energy"),
                                1,
                                true,
                                false,
                                null,
                                false,
                                false,
                                new RecurOptions(
                                        1,
                                        null,
                                        null,
                                        -1
                                ),
                                0.12,
                                250000.0,
                                null,
                                null,
                                "kWh"
                        ),
                        new Bcn(
                                3,
                                List.of(0),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Maintenance",
                                List.of("OMR"),
                                1,
                                true,
                                false,
                                null,
                                false,
                                false,
                                new RecurOptions(
                                        1,
                                        null,
                                        null,
                                        -1
                                ),
                                7000.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                4,
                                List.of(0),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Capital Equipment Residual Value",
                                List.of("Salvage Value"),
                                20,
                                true,
                                true,
                                null,
                                true,
                                true,
                                null,
                                3500.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                5,
                                List.of(1),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "HVAC System - High Efficiency",
                                List.of("Initial Investment"),
                                0,
                                true,
                                true,
                                20,
                                false,
                                false,
                                null,
                                130000.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                6,
                                List.of(1),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Fan Replacement",
                                List.of("Replacement Costs"),
                                12,
                                true,
                                true,
                                null,
                                false,
                                false,
                                null,
                                12500.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                7,
                                List.of(1),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Electricity",
                                List.of("Energy"),
                                1,
                                true,
                                false,
                                null,
                                false,
                                false,
                                new RecurOptions(
                                        1,
                                        null,
                                        null,
                                        -1
                                ),
                                0.12,
                                200000.0,
                                null,
                                null,
                                "kWh"
                        ),
                        new Bcn(
                                8,
                                List.of(1),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Maintenance",
                                List.of("OMR"),
                                1,
                                true,
                                false,
                                null,
                                false,
                                false,
                                new RecurOptions(
                                        1,
                                        null,
                                        null,
                                        20
                                ),
                                8000.0,
                                1.0,
                                null,
                                null,
                                null
                        ),
                        new Bcn(
                                9,
                                List.of(1),
                                BcnType.COST,
                                BcnSubType.DIRECT,
                                "Capital Equipment Residual Value",
                                List.of("Residual Value"),
                                20,
                                true,
                                true,
                                null,
                                true,
                                true,
                                null,
                                3700.0,
                                1.0,
                                null,
                                null,
                                null
                        )
                )
        );

        e3.analyze(input);
    }*/
}