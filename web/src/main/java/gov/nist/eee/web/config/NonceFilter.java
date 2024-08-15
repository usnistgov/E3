package gov.nist.eee.web.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpServletResponseWrapper;
import org.apache.commons.lang3.StringUtils;
import org.springframework.web.filter.GenericFilterBean;

import java.io.IOException;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.function.BiConsumer;

/**
 * Filter for injecting a nonce value into the CSP header.
 */
public class NonceFilter extends GenericFilterBean {
    public static final Base64.Encoder ENCODER = Base64.getEncoder();
    public static final String CSP_HEADER = "Content-Security-Policy";
    private static final int NONCE_SIZE = 64;
    private static final String CSP_NONCE_ATTRIBUTE = "cspNonce";

    private final SecureRandom random = new SecureRandom();

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        if (response instanceof HttpServletResponse httpResponse) {
            var nonceRandom = new byte[NONCE_SIZE];
            random.nextBytes(nonceRandom);

            var nonce = ENCODER.encodeToString(nonceRandom);
            request.setAttribute(CSP_NONCE_ATTRIBUTE, nonce);

            chain.doFilter(request, new CSPNonceResponseWrapper(httpResponse, nonce));
        } else {
            throw new ServletException("Could not apply CSP nonce filter");
        }
    }

    public static class CSPNonceResponseWrapper extends HttpServletResponseWrapper {
        private final String nonce;

        public CSPNonceResponseWrapper(HttpServletResponse response, String nonce) {
            super(response);
            this.nonce = nonce;
        }

        @Override
        public void setHeader(String name, String value) {
            replaceNonce(super::setHeader, name, value);
        }

        @Override
        public void addHeader(String name, String value) {
            replaceNonce(super::addHeader, name, value);
        }

        public void replaceNonce(BiConsumer<String, String> headerFunction, String name, String value) {
            if (validHeader(name, value))
                headerFunction.accept(name, value.replace("{nonce}", nonce));
            else
                headerFunction.accept(name, value);
        }

        private boolean validHeader(String name, String value) {
            return name.equals(CSP_HEADER) && StringUtils.isNotBlank(value);
        }
    }
}
