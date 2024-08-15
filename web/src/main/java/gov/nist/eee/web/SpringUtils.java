package gov.nist.eee.web;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.client.authentication.OAuth2AuthenticationToken;

public class SpringUtils {
    private SpringUtils() {
        throw new UnsupportedOperationException("Cannot instantiate static utility class");
    }

    /**
     * Obtains the name of the currently logged-in OAuth2 user.
     *
     * @return the name of the currently logged in OAuth2 user.
     */
    public static String getCurrentOAuth2UserName() {
        var oauth2Token = (OAuth2AuthenticationToken) SecurityContextHolder.getContext().getAuthentication();
        return oauth2Token.getName();
    }

    /**
     * Obtains the email of the currently logged-in OAuth2 user.
     *
     * @return the email of the currently logged in OAuth2 user.
     */
    public static String getCurrentOAuth2UserEmail() {
        var oauth2Token = (OAuth2AuthenticationToken) SecurityContextHolder.getContext().getAuthentication();
        return oauth2Token.getPrincipal().getAttribute("email");
    }
}
