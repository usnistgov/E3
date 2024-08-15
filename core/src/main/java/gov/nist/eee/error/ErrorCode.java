package gov.nist.eee.error;

public enum ErrorCode implements IErrorCode {
    E0000_UNREACHABLE(0x0000, "This region is unreachable in normal execution.");
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
