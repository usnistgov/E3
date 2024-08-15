package gov.nist.eee.web;

/*import gov.nist.e3.web.exceptions.ApiTokenException;*/
import gov.nist.eee.web.exceptions.ApiTokenException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;

@RestControllerAdvice
public class ExceptionTranslator {
    /**
     * Exception handler for validation errors caused by method parameters @RequesParam, @PathVariable, @RequestHeader
     * annotated with javax.validation constraints.
     */
    @ExceptionHandler
    protected ResponseEntity<E3Error> handleMethodArgumentNotValidException(MethodArgumentNotValidException exception) {
        var errors = new ArrayList<String>();
        for (var error : exception.getAllErrors()) {
            errors.add("Error validation object \"" + error.getObjectName() + "\", " + Arrays.toString(error.getArguments()));
        }

        return ResponseEntity.badRequest().body(new E3Error(
                E3ErrorType.VALIDATION_ERROR,
                LocalDateTime.now(),
                HttpStatus.BAD_REQUEST,
                errors.toString()
        ));
    }

    @ExceptionHandler
    protected ResponseEntity<E3Error> handleJsonParseError(HttpMessageNotReadableException exception) {
        return ResponseEntity.badRequest().body(
                new E3Error(
                        E3ErrorType.PARSE_ERROR,
                        LocalDateTime.now(),
                        HttpStatus.BAD_REQUEST,
                        exception.getCause().getMessage()
                )
        );
    }

    @ExceptionHandler
    protected ResponseEntity<E3Error> handleJsonParseError(ApiTokenException exception) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                new E3Error(
                        E3ErrorType.API_TOKEN_ERROR,
                        LocalDateTime.now(),
                        HttpStatus.UNAUTHORIZED,
                        exception.getMessage()
                )
        );
    }
}
