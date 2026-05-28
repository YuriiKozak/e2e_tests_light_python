import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.conftest import Configs

target_project = "Popopo"


@pytest.fixture(scope="function")
def login(page: Page, configs: Configs):
    open_home_page(page, configs)
    login_user(page, configs.email, configs.password)


def test_open_home_page_and_login(page: Page, login):
    expect(page.get_by_role("heading", name="Projects")).to_be_visible()


def test_open_home_page_and_login_with_invalid_credentials(page: Page, configs: Configs):
    open_home_page(page, configs)

    password = Faker().password(length=10)
    print(f"Generated random password: {password}")
    login_user(page, configs.email, password)

    expect(page.locator("#content-desktop").get_by_text("Invalid email or password")).to_be_visible()


def test_search_project(page: Page, login):
    expect(page.get_by_role("heading", name="Projects")).to_be_visible()

    search_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_visible()


def test_open_free_project(page: Page, login):
    expect(page.get_by_role("heading", name="Projects")).to_be_visible()

    page.locator("#company_id").select_option("Free Projects")

    search_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10_000)


def search_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.locator("#content-desktop #user_remember_me").click()
    page.get_by_role("button", name="Sign in").click()


def open_home_page(page: Page, configs: Configs):
    page.goto(configs.url)
    expect(page).to_have_title("Testomat.io")
