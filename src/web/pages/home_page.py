from typing import Self

import allure
from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Open Home Page")
    def open(self) -> Self:
        self.page.goto("https://testomat.io")
        return self

    @allure.step("Verify Home Page is loaded")
    def is_loaded(self) -> Self:
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item", has_text="Log in")).to_be_visible()
        expect(self.page.locator(".side-menu .start-item", has_text="Start for free")).to_be_visible()
        return self

    @allure.step("Click 'Log in' button")
    def click_login(self) -> Self:
        self.page.get_by_text("Log in", exact=True).click()
        return self
