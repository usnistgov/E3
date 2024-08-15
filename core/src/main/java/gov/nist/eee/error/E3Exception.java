package gov.nist.eee.error;

public class E3Exception extends RuntimeException {
    private final IErrorCode errorCode;
    private final String context;

    public E3Exception(IErrorCode errorCode) {
        super();
        this.errorCode = errorCode;
        this.context = "";
    }

    public E3Exception(IErrorCode errorCode, String context) {
        super();
        this.errorCode = errorCode;
        this.context = context;
    }

    public IErrorCode code() {
        return errorCode;
    }

    @Override
    public String getMessage() {
        return errorCode.getFullMessage() + '\n' + context;
    }
}
