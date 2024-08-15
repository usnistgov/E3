package gov.nist.eee.validation;

public class Result {
    public static class Success extends Result {

    }

    public static class Failure extends Result {
        private final String message;

        public Failure(final String message) {
            this.message = message;
        }

        public String getMessage() {
            return message;
        }
    }

}
