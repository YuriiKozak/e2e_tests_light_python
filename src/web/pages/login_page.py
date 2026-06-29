from typing import Self

import allure
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Open Login Page")
    def open(self) -> Self:
        self.page.goto("/users/sign_in")
        return self

    @allure.step("Verify Login Page is loaded")
    def is_loaded(self) -> Self:
        expect(self.page.locator("#content-desktop form#new_user")).to_be_visible()
        return self

    @allure.step("Log in with email: {email}")
    def login(self, email: str, password: str) -> Self:
        self.page.locator("#content-desktop #user_email").fill(email)
        self.page.locator("#content-desktop #user_password").fill(password)
        self.page.locator("#content-desktop #user_remember_me").click()
        self.page.get_by_role("button", name="Sign in").click()
        return self

    @allure.step("Verify invalid login error message is visible")
    def invalid_login_message_visible(self) -> Self:
        expect(self.page.locator("#content-desktop").get_by_text("Invalid email or password")).to_be_visible()
        return self
