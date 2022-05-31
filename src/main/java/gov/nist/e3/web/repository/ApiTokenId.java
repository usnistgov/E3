package gov.nist.e3.web.repository;

import javax.persistence.Id;
import java.io.Serializable;
import java.util.Objects;

/**
 * Class that represents the multi-column key for the API tokens.
 */
public class ApiTokenId implements Serializable {
    @Id
    String token;

    @Id
    String username;

    public ApiTokenId() {
    }

    public ApiTokenId(final String token, final String username) {
        this.token = token;
        this.username = username;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ApiTokenId that = (ApiTokenId) o;
        return Objects.equals(token, that.token) && Objects.equals(username, that.username);
    }

    @Override
    public int hashCode() {
        return Objects.hash(token, username);
    }
}
