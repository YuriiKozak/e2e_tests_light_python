from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage
from src.web.selenium.core.waits import Locator


class LoginPage(BasePage):
    EMAIL_INPUT: Locator = (By.CSS_SELECTOR, "#content-desktop #user_email")
    PASSWORD_INPUT: Locator = (
        By.CSS_SELECTOR,
        "#content-desktop #user_password",
    )
    REMEMBER_ME_CHECKBOX: Locator = (By.CSS_SELECTOR, "#user_remember_me")
    SIGN_IN_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "#content-desktop [value='Sign In']",
    )
    SUCCESS_MESSAGE: Locator = (
        By.CSS_SELECTOR,
        "#content-desktop .common-flash-success",
    )
    ERROR_MESSAGE: Locator = (
        By.CSS_SELECTOR,
        "#content-desktop .common-flash-alert",
    )
    INVALID_LOGIN_TEXT: Locator = (
        By.XPATH,
        "//*[contains(text(), 'Invalid Email or password')]",
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self, base_url: str = "") -> Self:
        self.driver.get(f"{base_url}/users/sign_in")
        return self

    def is_loaded(self) -> Self:
        self.wait.for_visible(self.EMAIL_INPUT)
        return self

    def check_remember_me(self) -> Self:
        checkbox = self.find(self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def click_sign_in(self) -> Self:
        return self

    def login(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.type_text(target=self.EMAIL_INPUT, text=email)
        self.type_text(target=self.PASSWORD_INPUT, text=password)

        if remember_me:
            self.check_remember_me()

        self.click(self.SIGN_IN_BUTTON)
        return self

    def should_see_success_message(self) -> Self:
        self.wait.for_visible(self.SUCCESS_MESSAGE)
        return self

    def should_see_invalid_login_error(self) -> Self:
        self.wait.for_visible(self.INVALID_LOGIN_TEXT)
        return self
