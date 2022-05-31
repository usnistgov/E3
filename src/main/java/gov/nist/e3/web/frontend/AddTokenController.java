package gov.nist.e3.web.frontend;

import gov.nist.e3.web.SpringUtils;
import gov.nist.e3.web.repository.ApiToken;
import gov.nist.e3.web.repository.ApiTokenRepository;
import org.apache.commons.lang3.RandomStringUtils;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.UUID;

@Controller
public class AddTokenController {
    private static final Logger log = LoggerFactory.getLogger(AddTokenController.class);

    private static final BCryptPasswordEncoder ENCODER = new BCryptPasswordEncoder();
    private static final String GOTO_DASHBOARD = "redirect:/dashboard";
    private static final int MAX_PREFIX_GENERATION_RETRIES = 1000;

    @Autowired
    ApiTokenRepository repository;

    @GetMapping("/token/create")
    public String createToken() {
        return "add";
    }

    /**
     * Resource for creating a new API token. This accepts a POST request with the name, expiry date, and expiry time
     * and will create a new token with those given details. Expiry date and time can be null for no expiration and if
     * just time is null then the key will expire at 12:00am on the given expiry day.
     *
     * @param model      the view model to pass information to the template.
     * @param name       the name of the API token to be generated passed as a form value.
     * @param expiryDate the expiration date of the key passed as a form value. Null means no expiration.
     * @param expiryTime the time of expiration on the above expiration date passed as a form value. Null means 12:00am.
     * @return If any values are incorrect, the form is returned again, otherwise a confirmation page where the user can
     * copy the newly created token down is displayed.
     */
    @PostMapping("/token/create")
    public String createApiToken(
            Model model,

            @RequestParam
            String name,

            @DateTimeFormat(pattern = "MM/dd/yyyy")
            @RequestParam(name = "expiry-date", required = false)
            LocalDate expiryDate,

            @DateTimeFormat(pattern = "H:mm")
            @RequestParam(name = "expiry-time", required = false)
            LocalTime expiryTime
    ) {
        // Validate name
        if (name == null || name.equals(""))
            return "add";

        // Create UUID token and hash it
        var uuid = UUID.randomUUID();
        var hashed = ENCODER.encode(uuid.toString());

        var user = SpringUtils.getCurrentOAuth2UserName();
        var prefix = createPrefix();
        var expiryDateTime = getExpiryDateTime(expiryDate, expiryTime);

        var token = new ApiToken(hashed, user, prefix, name, LocalDateTime.now(), expiryDateTime, false);
        log.debug("Generated token {}", token);

        repository.save(token);

        model.addAttribute("token", uuid);
        model.addAttribute("prefix", prefix);

        return "confirm";
    }

    /**
     * Creates and returns a random prefix that is 12 characters long. If the same prefix already exists in the database
     * retry up to a maximum number of retires to create a prefix that does not already exist.
     *
     * @return a random alphanumeric character sequence to use as a token prefix.
     */
    private String createPrefix() {
        var prefix = RandomStringUtils.random(12, true, true);
        var prefixGenerationTries = 0;
        while (prefixGenerationTries <= MAX_PREFIX_GENERATION_RETRIES && repository.existsByPrefix(prefix)) {
            prefix = RandomStringUtils.random(12, true, true);
            prefixGenerationTries++;
        }

        return prefix;
    }

    /**
     * Creates the expiry date time object from the given inputs.
     *
     * @param date the expiration date. If null then the key does not expire.
     * @param time the expiration time. If null but date is not null the time will default to 00:00 or 12:00am.
     * @return the LocalDateTime object or null if there is the key does not expire.
     */
    private @Nullable LocalDateTime getExpiryDateTime(@Nullable LocalDate date, @Nullable LocalTime time) {
        if (date == null)
            return null;

        var nonNullTime = time != null ? time : LocalTime.of(0, 0);
        return LocalDateTime.of(date, nonNullTime);
    }

    /**
     * Revokes the token that is identified by the given prefix and belongs to the currently logged-in user.
     *
     * @param prefix the prefix that identifies the key to be revoked passed as a form value.
     * @return redirects to the key dashboard.
     */
    @PostMapping("/token/revoke")
    public String revokeApiToken(@RequestParam String prefix) {
        repository.revoke(prefix, SpringUtils.getCurrentOAuth2UserName());
        return GOTO_DASHBOARD;
    }

    /**
     * Deletes the token that is identified by the given prefix and belongs to the currently logged-in user.
     *
     * @param prefix the prefix that identifies the key to be revoked passed as a form value.
     * @return redirect to the key dashboard
     */
    @PostMapping("/token/delete")
    public String deleteApiToken(@RequestParam String prefix) {
        repository.deleteByPrefixAndUsername(prefix, SpringUtils.getCurrentOAuth2UserName());
        return GOTO_DASHBOARD;
    }
}
