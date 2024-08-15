package gov.nist.eee.web.frontend;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Controller that returns the index page.
 */
@Controller
public class IndexController {
    /**
     * Returns the index page.
     *
     * @return the index page template.
     */
    @GetMapping(value = {"/", "/index"})
    public String index() {
        return "index";
    }
}
