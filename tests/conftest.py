import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from src.web.Application import Application
from src.web.pages.LoginPage import LoginPage

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
        "slow_mo": 100,
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


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(page: Page, configs: Configs):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
