package gov.nist.e3.web.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * Database Access Object for API tokens.
 */
public interface ApiTokenRepository extends JpaRepository<ApiToken, ApiTokenId> {
    /**
     * Returns a list of all API tokens associated with the given username.
     *
     * @param username the username to filter tokens by.
     * @return a list of API tokens associated with the given user.
     */
    List<ApiToken> findByUsername(String username);

    /**
     * Checks if a row exists with the given prefix.
     *
     * @param prefix the prefix to check.
     * @return true if there is a token with the given prefix, otherwise false.
     */
    boolean existsByPrefix(String prefix);

    /**
     * Get the API token identified by the given prefix.
     *
     * @param prefix the prefix to get the token by.
     * @return an API token identified by the given prefix.
     */
    ApiToken getByPrefix(String prefix);

    /**
     * Sets the revoked boolean of the API token specified by the given prefix and username to true.
     *
     * @param prefix the prefix that identifies the API token to revoke.
     * @param username the useranem associated with the API token to revoke.
     */
    @Transactional
    @Modifying(clearAutomatically = true)
    @Query("UPDATE ApiToken t SET t.revoked = true where t.prefix = :prefix and t.username = :username")
    void revoke(@Param("prefix") String prefix, @Param("username") String username);

    /**
     * Deletes all API tokens associated with the given user.
     *
     * @param username the user to delete all tokens for.
     */
    @Transactional
    void deleteAllByUsername(String username);

    /**
     * Delete the API token specified by the given prefix and username.
     *
     * @param prefix the prefix that identifies the token to delete.
     * @param username the user that the token to delete is associated with.
     */
    @Transactional
    void deleteByPrefixAndUsername(String prefix, String username);
}
