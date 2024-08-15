package gov.nist.eee.pipeline.quantity;

import gov.nist.eee.error.IErrorCode;

public enum ErrorCode implements IErrorCode {
    E7101_BCN_INITIAL_AFTER_END(0x7101, "A BCN's initial occurrence cannot occur after its end point."),
    E7102_INFLATE_LESS_THAN_ONE(0x7102, "Cannot inflate list with fewer than 1 elements."),
    E7103_VAR_VALUE_NULL(0x7103, "Cannot inflate with null var value."),
    E7104_PARTIALLY_DEFINED_VAR_VALUE(0x7104, "A BCN's quantity var value must either only have one element, or a number of elements equal to the study period");

    private final int code;
    private final String message;

    ErrorCode(int code, String message) {
        this.code = code;
        this.message = message;
    }

    @Override
    public int getCode() {
        return this.code;
    }

    @Override
    public String getMessage() {
        return this.message;
    }
}
