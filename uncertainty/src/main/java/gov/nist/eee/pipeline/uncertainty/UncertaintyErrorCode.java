package gov.nist.eee.pipeline.uncertainty;

import gov.nist.eee.error.IErrorCode;

public enum UncertaintyErrorCode implements IErrorCode {
    E0003_NO_VARIABLE_IN_TREE(0x0003, "The requested uncertainty variable was not in the request.");
    private final int code;
    private final String message;

    UncertaintyErrorCode(int code, String message) {
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
