from typing import Self

import allure
from playwright.sync_api import Page, expect


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Verify Projects Page is loaded")
    def is_loaded(self) -> Self:
        expect(self.page.get_by_role("heading", name="Projects")).to_be_visible()
        return self

    @allure.step("Select company/project: {target_project}")
    def select_project(self, target_project: str) -> Self:
        self.page.locator("#company_id").select_option(target_project)
        return self

    @allure.step("Search for project: {target_project}")
    def search_project(self, target_project: str) -> Self:
        expect(self.page.get_by_role("searchbox", name="search")).to_be_visible()
        self.page.locator("#content-desktop #search").fill(target_project)
        return self

    @allure.step("Verify search result shows project: {target_project}")
    def result_project(self, target_project: str) -> Self:
        expect(self.page.get_by_role("heading", name=target_project)).to_be_visible()
        return self

    @allure.step("Verify project is hidden: {target_project}")
    def project_is_hidden(self, target_project: str) -> Self:
        expect(self.page.get_by_role("heading", name=target_project)).to_be_hidden()
        return self

    @allure.step("Verify empty state message is visible")
    def empty_state_is_visible(self) -> Self:
        expect(
            self.page.get_by_text("You have not created any projects yet")
        ).to_be_visible()
        return self
