package gov.nist.eee.web.api;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import org.jetbrains.annotations.Nullable;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Objects;
import java.util.StringJoiner;

/**
 * Class that represents an API token.
 */
@Entity
@IdClass(ApiTokenId.class)
public class ApiToken {
    /**
     * The actual string that acts as a password for this token. This value should be hashed.
     */
    @Id
    String token;

    /**
     * The OAuth2 username for the user that owns this API token.
     */
    @Id
    String username;

    /**
     * A unique random string used to identify this token. Stored in plain text.
     */
    @Column(unique = true)
    String prefix;

    /**
     * The user readable name of this token.
     */
    String name;

    /**
     * The date and time that this token was created. This is only for the user's information
     */
    LocalDateTime created;

    /**
     * The date and time that this token expires. If this is null then the token never expires.
     */
    @Nullable
    LocalDateTime expiry;

    /**
     * True if this token has been manually revoked by a user, otherwise false.
     */
    boolean revoked;

    public ApiToken() {
    }

    public ApiToken(
            String token,
            String user,
            String prefix,
            String name,
            LocalDateTime created,
            @Nullable LocalDateTime expiry,
            boolean revoked
    ) {
        this.token = token;
        this.username = user;
        this.prefix = prefix;
        this.name = name;
        this.created = created;
        this.expiry = expiry;
        this.revoked = revoked;
    }

    public String getToken() {
        return token;
    }

    public String getUsername() {
        return username;
    }

    public String getPrefix() {
        return prefix;
    }

    public String getName() {
        return name;
    }

    public LocalDateTime getCreated() {
        return created;
    }

    public @Nullable LocalDateTime getExpiry() {
        return expiry;
    }

    public boolean isRevoked() {
        return revoked;
    }

    /**
     * Returns the current status of this API token. Can be ACTIVE, EXPIRED, or REVOKED.
     * Revoked takes precedence over expired.
     *
     * @return the current status of this token.
     */
    public ApiTokenStatus getStatus() {
        if (revoked)
            return ApiTokenStatus.REVOKED;

        if (expiry != null && LocalDateTime.now().isAfter(expiry))
            return ApiTokenStatus.EXPIRED;

        return ApiTokenStatus.ACTIVE;
    }

    /**
     * Returns the creation date formatted as "mm/dd/yyyy".
     *
     * @return the creation date as a formatted string.
     */
    public String getFormattedCreated() {
        return created.format(DateTimeFormatter.ofPattern("M/d/y"));
    }

    /**
     * Returns the expiration date formatted as "mm/dd/yyyy hh:mm am/pm"
     *
     * @return the expiration date as a formatted string.
     */
    public String getFormattedExpiry() {
        if (expiry == null)
            return "";

        return expiry.format(DateTimeFormatter.ofPattern("M/d/y h:mma"));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ApiToken apiToken = (ApiToken) o;
        return revoked == apiToken.revoked && Objects.equals(token, apiToken.token) && Objects.equals(username, apiToken.username) && Objects.equals(name, apiToken.name) && Objects.equals(created, apiToken.created) && Objects.equals(expiry, apiToken.expiry);
    }

    @Override
    public int hashCode() {
        return Objects.hash(token, username, name, created, expiry, revoked);
    }

    @Override
    public String toString() {
        return new StringJoiner(", ", ApiToken.class.getSimpleName() + "[", "]")
                .add("prefix=" + prefix)
                .add("token=" + token)
                .add("username='" + username + "'")
                .add("name='" + name + "'")
                .add("created=" + created)
                .add("expiry=" + expiry)
                .add("revoked=" + revoked)
                .toString();
    }
}
