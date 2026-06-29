from typing import Self

import allure
from playwright.sync_api import Page, expect

from src.web.components.sidebar import Sidebar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = Sidebar(page)

    @allure.step("Verify Project Page is loaded")
    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible()
        expect(self.page.locator(".mainnav-menu")).to_be_visible()
        expect(self.page.locator("[placeholder = 'First Suite']")).to_be_visible()
        expect(self.page.get_by_role("button", name="Suite")).to_be_visible()
        return self

    @allure.step("Verify project title is: {expected_project_title}")
    def project_title_is(self, expected_project_title: str) -> Self:
        expect(
            self.page.get_by_role("heading", name=expected_project_title)
        ).to_be_visible()
        return self

    @allure.step("Close README panel")
    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self
