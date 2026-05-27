import re
from typing import Self

from playwright.sync_api import Page, expect, Locator

from src.web.components.SidebarTabEnum import SidebarTab


class SideBar:
    def __init__(self, page: Page):
        self.page = page

        self.container = page.locator(".mainnav-menu")

        self.open_button = self.container.locator("button.btn-open")
        self.close_button = self.container.locator("button.btn-close")

        self.tests_link = self.container.get_by_role("link", name="Tests")
        self.requirements_link = self.container.get_by_role("link", name="Requirements")
        self.runs_link = self.container.get_by_role("link", name="Runs")
        self.plans_link = self.container.get_by_role("link", name="Plans")
        self.steps_link = self.container.get_by_role("link", name="Steps")
        self.pulse_link = self.container.get_by_role("link", name="Pulse")
        self.imports_link = self.container.get_by_role("link", name="Imports")
        self.analytics_link = self.container.get_by_role("link", name="Analytics")
        self.branches_link = self.container.get_by_role("link", name="Branches")
        self.settings_link = self.container.get_by_role("link", name="Settings")

        self.help_link = self.container.get_by_role("link", name="Help")
        self.projects_link = self.container.get_by_role("link", name="Projects")
        self.user_profile_link = self.container.get_by_role("link", name="Yurii Kozak")

    @property
    def _tab_mapping(self) -> dict[SidebarTab, Locator]:
        return {
            SidebarTab.TESTS: self.tests_link,
            SidebarTab.REQUIREMENTS: self.requirements_link,
            SidebarTab.RUNS: self.runs_link,
            SidebarTab.PLANS: self.plans_link,
            SidebarTab.STEPS: self.steps_link,
            SidebarTab.PULSE: self.pulse_link,
            SidebarTab.IMPORTS: self.imports_link,
            SidebarTab.ANALYTICS: self.analytics_link,
            SidebarTab.BRANCHES: self.branches_link,
            SidebarTab.SETTINGS: self.settings_link,
            SidebarTab.HELP: self.help_link,
            SidebarTab.PROJECTS: self.projects_link,
            SidebarTab.PROFILE: self.user_profile_link,
        }

    def is_loaded(self) -> Self:
        expect(self.container).to_be_visible()
        return self

    def open(self) -> Self:
        self.open_button.click()
        expect(self.open_button).to_be_hidden()
        expect(self.close_button).to_be_visible()
        return self

    def close(self) -> Self:
        self.close_button.click()
        expect(self.close_button).to_be_hidden()
        expect(self.open_button).to_be_visible()
        return self

    def navigate_to(self, target: SidebarTab) -> Self:
        self._tab_mapping.get(target).click()
        return self

    def is_tab_active(self, target: SidebarTab) -> Self:
        self.page.wait_for_timeout(500)
        expect(self._tab_mapping.get(target)).to_have_class(re.compile(r"\bactive\b"))
        return self
