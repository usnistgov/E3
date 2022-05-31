package gov.nist.e3.web.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.web.header.HeaderWriterFilter;

@Configuration
@PropertySource("classpath:oauth2.properties")
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.cors()
                .and()
                .authorizeRequests()
                // public endpoints
                .antMatchers("/", "/documentation/", "/manual/", "/api/**").permitAll()
                // static resources
                .antMatchers("/css/**", "/js/**", "/img/**", "/uswds-2.13.2/**").permitAll()
                // default authenticated
                .anyRequest().authenticated()
                .and()
                .oauth2Login()
                .and()
                .logout().logoutSuccessUrl("/").logoutUrl("/logout")
                .and()
                .csrf().disable()
                .addFilterBefore(new NonceFilter(), HeaderWriterFilter.class)
                .headers()
                .xssProtection()
                .and()
                .contentSecurityPolicy(
                        "script-src-elem 'self' cdn.jsdelivr.net accounts.google.com 'nonce-{nonce}'"
                );
    }
}
