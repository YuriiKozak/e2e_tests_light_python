from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

Locator = tuple[By, str]
LocatorOrElement = Locator | WebElement


class Wait:
    DEFAULT_TIMEOUT = 10
    DEFAULT_POLL = 0.2
    IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(
            driver=driver,
            timeout=timeout,
            poll_frequency=self.DEFAULT_POLL,
            ignored_exceptions=self.IGNORED_EXCEPTIONS,
        )

    def _is_locator(self, target: LocatorOrElement) -> bool:
        return isinstance(target, tuple) and len(target) == 2

    def for_visible(
        self, target: LocatorOrElement, custom_timeout: int = None
    ) -> WebElement:
        """Waits until element is visible, using custom timeout"""
        if custom_timeout:
            self._wait = WebDriverWait(
                driver=self.driver,
                timeout=custom_timeout,
                poll_frequency=self.DEFAULT_POLL,
            )
        if self._is_locator(target):
            return self._wait.until(EC.visibility_of_element_located(target))

        return self._wait.until(EC.visibility_of(target))

    def for_invisible(self, target: LocatorOrElement) -> bool | WebElement:
        if self._is_locator(target):
            return self._wait.until(EC.invisibility_of_element_located(target))

        return self._wait.until(EC.invisibility_of_element(target))

    def for_present(self, locator: Locator) -> WebElement:
        return self._wait.until(EC.presence_of_element_located(locator))

    def for_all_present(self, locator: Locator) -> list[WebElement]:
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    def for_clickable(self, target: LocatorOrElement) -> WebElement:
        if self._is_locator(target):
            return self._wait.until(EC.element_to_be_clickable(target))

        return self._wait.until(EC.element_to_be_clickable(target))

    def for_text_present(self, target: LocatorOrElement, text: str) -> bool:
        if self._is_locator(target):
            return self._wait.until(
                EC.text_to_be_present_in_element(locator=target, text_=text)
            )

        return self._wait.until(lambda d: text in target.text)

    def for_selected(self, target: LocatorOrElement) -> bool:
        if self._is_locator(target):
            return self._wait.until(EC.element_located_to_be_selected(target))

        return self._wait.until(EC.element_to_be_selected(target))

    def for_stale(self, element: WebElement) -> bool:
        return self._wait.until(EC.staleness_of(element))

    def for_frame(self, target: LocatorOrElement) -> bool:
        if self._is_locator(target):
            return self._wait.until(EC.frame_to_be_available_and_switch_to_it(target))

        return self._wait.until(EC.frame_to_be_available_and_switch_to_it(target))

    def until(self, condition):
        return self._wait.until(condition)

    def until_not(self, condition):
        return self._wait.until_not(condition)
