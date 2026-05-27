from typing import Self

from playwright.sync_api import Page, expect


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

    def is_loaded(self) -> Self:
        expect(self.page.locator(".sticky-header")).to_be_visible()
        expect(self.page.locator(".mainnav-menu")).to_be_visible()
        expect(self.page.locator("[placeholder = 'First Suite']")).to_be_visible()
        expect(self.page.get_by_role("button", name="Suite")).to_be_visible()
        return self

    def project_title_is(self, expected_project_title: str) -> Self:
        expect(self.page.get_by_role("heading", name=expected_project_title)).to_be_visible()
        return self

    def close_read_me(self) -> Self:
        self.page.locator(".back .third-btn").click()
        return self
