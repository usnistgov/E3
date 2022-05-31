package gov.nist.e3.web;

import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;

/**
 * Record that contains information for when an error occurs in an E3 request. This information is sent back to the
 * user for diagnostic purposes.
 *
 * @param type The type of error that occurred.
 * @param timestamp The timestamp at which the error occurred.
 * @param status The http status associated with the message. Most likely 400 Bad Request.
 * @param message The messages that the error generates
 */
public record E3Error(E3ErrorType type, LocalDateTime timestamp, HttpStatus status, String message) {
}
