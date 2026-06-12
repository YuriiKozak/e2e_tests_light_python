from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import BrowserContext, Page
from playwright.sync_api import Error as PlaywrightError

from src.web.application import Application
from tests.fixtures.config import Configs

# Path to the saved authentication state
STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")


# ==============================================================================
# 1. Base Browser Configurations (Session Scope)
# ==============================================================================


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, configs: Configs) -> dict:
    """
    Configures default browser context arguments dynamically.
    Utilizes base_url retrieved from environment configurations.
    """
    args = {
        **browser_context_args,
        "base_url": configs.url,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "permissions": ["geolocation"],
    }
    if STORAGE_STATE_PATH.exists():
        args["storage_state"] = str(STORAGE_STATE_PATH)
    return args


# ==============================================================================
# 2. Standard Authenticated Fixtures (Function Scope)
# ==============================================================================


@pytest.fixture(scope="function")
def context(
    browser, browser_context_args: dict
) -> Generator[BrowserContext, None, None]:
    """
    Overrides the default Playwright context fixture to dynamically load storage state if it exists.
    This ensures that tests executing in the same session can share state even if the
    storage state file was created after the session started.
    """
    args = {**browser_context_args}
    if STORAGE_STATE_PATH.exists():
        args["storage_state"] = str(STORAGE_STATE_PATH)
    context = browser.new_context(**args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    """Provides access to the Application page objects using the standard, potentially authenticated page."""
    return Application(page)


@pytest.fixture(scope="function")
def login(configs: Configs, app: Application) -> None:
    """
    Fixture to perform a standard user login.
    Leverages the Page Object Pattern for maintainability.
    Saves authentication state upon successful login or bypasses if already logged in.
    """
    if STORAGE_STATE_PATH.exists():
        app.page.goto("/projects")
        return

    (app.login_page.open().is_loaded().login(configs.email, configs.password))
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    app.page.context.storage_state(path=STORAGE_STATE_PATH)


# ==============================================================================
# 3. Clean / Unauthenticated Fixtures (Function Scope)
# ==============================================================================


@pytest.fixture(scope="function")
def clean_context(
    browser, browser_context_args: dict
) -> Generator[BrowserContext, None, None]:
    """Provides a fresh, unauthenticated browser context by stripping any storage state."""
    args = {**browser_context_args}
    args.pop("storage_state", None)
    context = browser.new_context(**args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def clean_page(clean_context: BrowserContext) -> Generator[Page, None, None]:
    """Provides a fresh, unauthenticated browser page."""
    page = clean_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def clean_app(clean_page: Page) -> Application:
    """Provides an Application instance with a fresh, unauthenticated browser page (e.g. for login testing)."""
    return Application(clean_page)


# ==============================================================================
# 4. Module-Scoped Shared Fixtures (Clean / Unauthenticated)
# ==============================================================================


@pytest.fixture(scope="module")
def session_context(
    browser, browser_context_args: dict
) -> Generator[BrowserContext, None, None]:
    """Module-scoped browser context to avoid reopening the browser between tests. Forces clean state."""
    args = {**browser_context_args}
    args.pop("storage_state", None)
    context = browser.new_context(**args)
    yield context
    context.close()


@pytest.fixture(scope="module")
def session_page(session_context: BrowserContext) -> Generator[Page, None, None]:
    """Module-scoped browser page to reuse the same tab across multiple tests."""
    page = session_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def session_app(session_page: Page) -> Application:
    """Provides access to the Application page objects using the shared, module-scoped page."""
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


# ==============================================================================
# 5. Pytest Execution Hooks
# ==============================================================================


def pytest_collection_modifyitems(items):
    """
    Stably sorts collected test items by their file path and defined line number
    to ensure stable, sequential execution order and prevent splitting.
    """
    items.sort(key=lambda item: (item.location[0], item.location[1]))
