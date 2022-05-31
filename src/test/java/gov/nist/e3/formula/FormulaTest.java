package gov.nist.e3.formula;

import net.jqwik.api.ForAll;
import net.jqwik.api.Property;
import net.jqwik.api.constraints.DoubleRange;
import net.jqwik.api.constraints.Negative;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.Test;

import java.util.List;

import static gov.nist.e3.formula.Formula.*;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import static org.hamcrest.core.Is.is;

class FormulaTest {
    @Test
    void compoundTestCases() {
        assertThat(compound(5.0, 9.0), is(equalTo(50.0)));
        assertThat(compound(1.2, 10.3), is(equalTo(13.56)));
        assertThat(compound(-7.4, 5.3), is(equalTo(-46.62)));
    }

    @Property
    void compoundAddsOneToCurrent(@ForAll double current) {
        assertThat(compound(1.0, current), is(equalTo(current + 1.0)));
    }

    @Property
    void compoundReturnsPreviousIfCurrentIsZero(@ForAll double previous) {
        assertThat(compound(previous, 0.0), is(equalTo(previous)));
    }

    @Property
    void compoundReturnsZeroIfPreviousIsZero(@ForAll double current) {
        assertThat(compound(0.0, current), anyOf(equalTo(-0.0), equalTo(0.0)));
    }

    @Property
    void presentValueIsZeroIfValueIsZero(@ForAll double rate, @ForAll double timeStep) {
        assertThat(presentValue(0.0, rate, timeStep), Matchers.is(equalTo(0.0)));
    }

    @Property
    void presentValueIsZeroIfTimeStepIsEqualToValue(@ForAll double value, @ForAll double rate) {
        assertThat(presentValue(value, rate, 0.0), Matchers.is(equalTo(value)));
    }

    @Property
    void presentValueIsZeroIfRateIsNegativeOneAndTimeStepIsNegative(
            @ForAll double value,
            @ForAll @Negative double timeStep
    ) {
        assertThat(presentValue(value, -1.0, timeStep), anyOf(equalTo(0.0), equalTo(-0.0)));
    }

    @Property
    void presentValueIsInfinityIfRateIsNegativeOneAndTimeStepIsPositive(
            @ForAll @DoubleRange(minIncluded = false) double value,
            @ForAll @DoubleRange(minIncluded = false) double timeStep
    ) {
        assertThat(presentValue(value, -1.0, timeStep), anyOf(equalTo(Double.POSITIVE_INFINITY), equalTo(Double.NEGATIVE_INFINITY)));
    }

    @Test
    void irrIsCorrect() {
 /*       var result = irr(List.of(-100.0, 39.0, 59.0, 55.0, 20.0));
        assertThat(result, is(closeTo(0.2809, 0.0001)));
        System.out.println(result);

        var result2 = irr(List.of(-100000.0, 50000.0, 30000.0, -20000.0, 130000.0));
        assertThat(result2, is(closeTo(0.2607, 0.0001)));
        System.out.println(result2);

        var result3 = irr(List.of(-100.0, 250.0));
        assertThat(result3, is(closeTo(1.4999, 0.0001)));
        System.out.println(result3);
*/

        var result4 = irr(List.of(-5.574E7, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602, 2120745.602));
        assertThat(result4, is(closeTo(0.0352, 0.0001)));
        System.out.println(result4);
    }
}