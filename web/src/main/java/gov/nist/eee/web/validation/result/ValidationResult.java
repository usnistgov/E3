package gov.nist.eee.web.validation.result;

public class ValidationResult {
    public static class Success extends ValidationResult {

    }

    public static class Failure extends ValidationResult {
        private final String message;

        public Failure(final String message) {
            this.message = message;
        }

        public String getMessage() {
            return message;
        }
    }

}
