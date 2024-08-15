package gov.nist.eee.web.api;

/**
 * Enum that specifies all valid statuses of an API token. Currently, a token can be ACTIVE, EXPIRED or REVOKED.
 * A token is only valid and can be used if it is ACTIVE.
 */
public enum ApiTokenStatus {
    ACTIVE, EXPIRED, REVOKED
}
