package gov.nist.e3.web.frontend;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Controller that serves the documentation page.
 */
@Controller
public class DocumentationController {
    /**
     * Returns the generated E3 request schema documentation.
     *
     * @return the documentation template.
     */
    @GetMapping("/documentation")
    public String login() {
        return "documentation";
    }
}

