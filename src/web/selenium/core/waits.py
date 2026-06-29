from typing import Any, Callable

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

Locator = tuple[str, str]
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

    def for_visible(self, target: LocatorOrElement, custom_timeout: int | None = None) -> WebElement:
        """Waits until element is visible, using custom timeout."""
        wait = self._wait
        if custom_timeout is not None:
            wait = WebDriverWait(
                driver=self.driver,
                timeout=custom_timeout,
                poll_frequency=self.DEFAULT_POLL,
                ignored_exceptions=self.IGNORED_EXCEPTIONS,
            )
        if isinstance(target, tuple):
            return wait.until(EC.visibility_of_element_located(target))

        return wait.until(EC.visibility_of(target))

    def for_invisible(self, target: LocatorOrElement) -> bool | WebElement:
        """Waits until element is invisible."""
        if isinstance(target, tuple):
            return self._wait.until(EC.invisibility_of_element_located(target))

        return self._wait.until(EC.invisibility_of_element(target))

    def for_present(self, locator: Locator) -> WebElement:
        """Waits until element is present in DOM."""
        return self._wait.until(EC.presence_of_element_located(locator))

    def for_all_present(self, locator: Locator) -> list[WebElement]:
        """Waits until all elements are present in DOM."""
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    def for_clickable(self, target: LocatorOrElement) -> WebElement | bool | tuple[str, str]:
        """Waits until element is clickable (visible and enabled)."""
        if isinstance(target, tuple):
            return self._wait.until(EC.element_to_be_clickable(target))

        return self._wait.until(lambda _: target if (target.is_displayed() and target.is_enabled()) else False)

    def for_text_present(self, target: LocatorOrElement, text: str) -> bool:
        """Waits until text is present in element."""
        if isinstance(target, tuple):
            return self._wait.until(EC.text_to_be_present_in_element(locator=target, text_=text))

        return self._wait.until(lambda _: text in target.text)

    def for_selected(self, target: LocatorOrElement) -> bool:
        """Waits until element is selected."""
        if isinstance(target, tuple):
            return self._wait.until(EC.element_located_to_be_selected(target))

        return self._wait.until(EC.element_to_be_selected(target))

    def for_stale(self, element: WebElement) -> bool:
        """Waits until element becomes stale."""
        return self._wait.until(EC.staleness_of(element))

    def for_frame(self, target: LocatorOrElement) -> bool:
        """Waits until frame is available and switches to it."""
        return self._wait.until(EC.frame_to_be_available_and_switch_to_it(target))

    def until(self, condition: Callable[[WebDriver], Any], message: str = "") -> Any:
        """Waits until the condition is met."""
        return self._wait.until(condition, message)

    def until_not(self, condition: Callable[[WebDriver], Any], message: str = "") -> Any:
        """Waits until the condition is not met."""
        return self._wait.until_not(condition, message)
