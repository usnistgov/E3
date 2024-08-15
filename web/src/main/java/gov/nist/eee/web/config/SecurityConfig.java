package gov.nist.eee.web.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.header.HeaderWriterFilter;
import org.springframework.web.cors.CorsConfiguration;

@Configuration
@PropertySource("classpath:oauth2.properties")
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
                .cors(Customizer.withDefaults())
                .authorizeHttpRequests(auth -> auth
                        // public endpoints
                        .requestMatchers("/", "/documentation/", "/manual/", "/api/**").permitAll()
                        // static resources
                        .requestMatchers("/css/**", "/js/**", "/img/**", "/uswds-2.13.2/**").permitAll()
                        // default authenticated
                        .anyRequest().authenticated()
                )
                .oauth2Login(Customizer.withDefaults())
                .csrf(AbstractHttpConfigurer::disable)
                .logout((logout) -> logout.logoutSuccessUrl("/").logoutUrl("/logout"))
                .addFilterBefore(new NonceFilter(), HeaderWriterFilter.class)
                .headers((headers) -> headers
                        .xssProtection(Customizer.withDefaults())
                        .contentSecurityPolicy((csp) -> csp.policyDirectives(
                                "script-src-elem 'self' cdn.jsdelivr.net accounts.google.com 'nonce-{nonce}'"
                        ))
                )
                .build();
    }
}
