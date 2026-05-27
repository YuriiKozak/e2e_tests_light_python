from ast import List

from playwright.sync_api import Page

from src.web.components.HeaderComponent import HeaderComponent
from src.web.components.ProjectCardComponent import ProjectCardComponent


class ProjectsPage:
    def __init__(self, page: Page):
        """Main Page Object managing the Header and Project Card components."""
        self.page = page

        # Initialize Header Component
        self.header = HeaderComponent(page.locator(".common-page-header"))

        # List items locator
        self.project_items = page.locator("#grid ul.grid > li")

        # Indicator element used to verify page loading status
        self.page_indicator = page.locator(".common-page-header-left h2")

    def is_loaded(self, timeout: float = 5000) -> bool:
        """Checks if the page is fully loaded by waiting for the page indicator to become visible."""
        try:
            self.page_indicator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def navigate(self, url: str = "/projects"):
        """Navigates to the projects URL and waits for the page to load completely."""
        self.page.goto(url)
        self.page_indicator.wait_for(state="visible")

    def get_all_projects(self) -> List[ProjectCardComponent]:
        """Returns a list of components for all currently visible project cards."""
        self.page_indicator.wait_for(state="visible")

        count = self.project_items.count()
        projects = []
        for i in range(count):
            card_locator = self.project_items.nth(i)
            # Checked for visibility since client-side search hides elements via display:none
            if card_locator.is_visible():
                projects.append(ProjectCardComponent(card_locator))
        return projects

    def get_project_by_title(self, title: str) -> ProjectCardComponent:
        """Finds and returns a specific project component by its exact title."""
        card_locator = self.project_items.filter(has=self.page.locator(f"h3:text-is('{title}')"))
        if card_locator.count() > 0:
            return ProjectCardComponent(card_locator.first)
        raise ValueError(f"Project with title '{title}' was not found on the page.")
