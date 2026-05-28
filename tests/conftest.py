import os
from dataclasses import dataclass
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, BrowserContext

from src.web.Application import Application

load_dotenv()


@dataclass(frozen=True)
class Configs:
    url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Configs(
        url=os.environ["URL"],
        email=os.environ["EMAIL"],
        password=os.environ["PASSWORD"]
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chromium",
        "headless": False,
        "slow_mo": 300,
        "timeout": 30000,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="session")
def context(browser, browser_context_args: dict) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="session")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function", autouse=True)
def clear_browser_state(page: Page):
    yield
    try:
        page.context.clear_cookies()
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        page.wait_for_timeout(2000)
    except PlaywrightError:
        pass


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(configs: Configs, app: Application):
    (app.login_page
     .open()
     .is_loaded()
     .login(configs.email, configs.password))
