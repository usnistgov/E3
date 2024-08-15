package gov.nist.eee.web.frontend;

import gov.nist.eee.web.SpringUtils;
import gov.nist.eee.web.api.ApiTokenRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Controller for displaying user dashboard and other account actions.
 */
@Controller
public class DashboardController {
    private static final Logger log = LoggerFactory.getLogger(DashboardController.class);

    private final ApiTokenRepository repository;

    public DashboardController(ApiTokenRepository repository) {
        this.repository = repository;
    }

    /**
     * Returns a webpage with a list of API tokens associated with the currently logged-in user.
     *
     * @param model the model used to pass values to the template engine.
     * @return the dashboard template.
     */
    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        var user = SpringUtils.getCurrentOAuth2UserName();
        var email = SpringUtils.getCurrentOAuth2UserEmail();

        model.addAttribute("username", email);
        model.addAttribute("tokens", repository.findByUsername(user));

        log.trace("Displaying dashboard for user {}", user);

        return "dashboard";
    }

    /**
     * Deletes all keys associated with the currently logged-in user. This is similar to completely deleting the
     * account with other services, however E3 only retains API keys so those are all that is deleted.
     *
     * @return the logout endpoint so users are immediately logged out after key deletion.
     */
    @GetMapping("/account/delete")
    public String deleteAccount() {
        var user = SpringUtils.getCurrentOAuth2UserName();
        repository.deleteAllByUsername(user);

        log.trace("Deleted keys associated with user {}", user);

        return "redirect:/logout";
    }
}