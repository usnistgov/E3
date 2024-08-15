package gov.nist.eee.error;

public interface IErrorCode {
    int getCode();

    String getMessage();

    default String getFullMessage() {
       return String.format("Error 0x%04X: %2s", this.getCode(), this.getMessage());
    }
}
