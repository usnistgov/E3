package gov.nist.eee.pipeline.sensitivity;

import gov.nist.eee.error.IErrorCode;

public enum SensitivityErrorCode implements IErrorCode {
    E0002_NO_VARIABLE_IN_TREE(0x0002, "The requested sensitivity variable was not in the request.");
    private final int code;
    private final String message;

    SensitivityErrorCode(int code, String message) {
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
