package gov.nist.eee.validation.error;

public class ValidatorCreationException extends RuntimeException {
    public ValidatorCreationException(String message, Exception cause) {
        super(message, cause);
    }
}
