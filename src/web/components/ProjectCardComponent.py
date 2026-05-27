from playwright.sync_api import Locator


class ProjectCardComponent:
    def __init__(self, locator: Locator):
        """Component for interacting with an individual project card in the grid."""
        self.locator = locator

        # Internal locators
        self.title_locator = locator.locator("h3")
        self.tests_count_locator = locator.locator("p.mt-1")
        self.badge_locator = locator.locator(".project-badges span")
        self.link_locator = locator.locator("a")
        self.extra_team_count = locator.locator("div.inline-flex div")

    @property
    def title(self) -> str:
        """Returns the project title (e.g., 'Gorgeous Plastic Lamp')."""
        return self.title_locator.inner_text().strip()

    @property
    def tests_count_text(self) -> str:
        """Returns the tests count string (e.g., '0 tests')."""
        return self.tests_count_locator.inner_text().strip()

    @property
    def badge_text(self) -> str:
        """Returns the project type badge text (e.g., 'Classical')."""
        return self.badge_locator.inner_text().strip()

    @property
    def additional_team_members_count(self) -> int:
        """Returns the number of extra team members (e.g., parses 42 from '+42')."""
        if self.extra_team_count.is_visible():
            text = self.extra_team_count.inner_text().strip()
            return int(text.replace("+", ""))
        return 0

    def click(self):
        """Clicks the project card link to open the project."""
        self.link_locator.click()
