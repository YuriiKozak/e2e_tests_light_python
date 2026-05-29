from typing import Generator

import pytest
from playwright.sync_api import BrowserContext, Page
from playwright.sync_api import Error as PlaywrightError

from src.web.application import Application
from tests.fixtures.config import Configs


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, configs: Configs) -> dict:
    """
    Configures the browser context dynamically.
    Utilizes base_url retrieved from environment configurations.
    """
    return {
        **browser_context_args,
        "base_url": configs.url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="module")
def session_context(
    browser, browser_context_args: dict
) -> Generator[BrowserContext, None, None]:
    """Module-scoped browser context to avoid reopening the browser between tests."""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="module")
def session_page(session_context: BrowserContext) -> Generator[Page, None, None]:
    """Module-scoped browser page to reuse the same tab across tests."""
    page = session_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def session_app(session_page: Page) -> Application:
    """Fixture providing access to the Application page objects using the shared session page."""
    return Application(session_page)


@pytest.fixture(scope="function", autouse=True)
def clear_session_page_state(request) -> Generator[None, None, None]:
    """
    Clears cookies, localStorage, and sessionStorage between tests to maintain state isolation,
    but only if the test actually used the session-scoped page.
    """
    if "session_page" in request.fixturenames or "session_app" in request.fixturenames:
        session_page = request.getfixturevalue("session_page")
        yield
        try:
            session_page.context.clear_cookies()
            session_page.evaluate(
                "() => { localStorage.clear(); sessionStorage.clear(); }"
            )
            session_page.wait_for_timeout(1000)
        except PlaywrightError:
            pass
    else:
        yield


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    """Fixture providing access to the Application page objects using a fresh page."""
    return Application(page)


@pytest.fixture(scope="function")
def login(configs: Configs, app: Application) -> None:
    """
    Fixture to perform a standard user login.
    Leverages the Page Object Pattern for maintainability.
    """
    (app.login_page.open().is_loaded().login(configs.email, configs.password))


def pytest_collection_modifyitems(items):
    """
    Stably sorts collected test items by their file path and defined line number
    to ensure stable, sequential execution order and prevent splitting.
    """
    items.sort(key=lambda item: (item.location[0], item.location[1]))
