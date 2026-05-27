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


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(page: Page, configs: Configs):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
