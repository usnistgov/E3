package gov.nist.eee.util;

import org.junit.jupiter.api.Test;

import gov.nist.eee.util.Result.Success;
import gov.nist.eee.util.Result.Failure;

class ResultTest {
    @Test
    void test() {
        var result = new Success<>(10);
        Result<Integer, IllegalArgumentException> fail = new Failure<>(new IllegalArgumentException("Not valid"));

        var result2 = result
                .map(integer -> integer * 2)
                .flatMap(integer -> {
                    if (integer == 0)
                        return new Failure<>(new ArithmeticException("Divide by 0"));

                    return new Success<>(1 / integer);
                });
        var fail2 = fail.map(value -> value * 2);

        System.out.println(result2);
        System.out.println(fail2);
    }
}