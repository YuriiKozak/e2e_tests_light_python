import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

URL = os.environ["URL"]
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]


def test_open_home_page_and_login(page: Page):
    open_home_page(page)
    login_user(page, EMAIL, PASSWORD)

    expect(page.get_by_role("heading", name="Projects")).to_be_visible()


def test_search_project(page: Page):
    open_home_page(page)
    login_user(page, EMAIL, PASSWORD)

    expect(page.get_by_role("heading", name="Projects")).to_be_visible()

    target_project = "Popopo"
    search_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_visible()


def test_open_free_project(page: Page):
    open_home_page(page)
    login_user(page, EMAIL, PASSWORD)

    expect(page.get_by_role("heading", name="Projects")).to_be_visible()

    page.locator("#company_id").select_option("Free Projects")

    target_project = "Popopo"
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


def open_home_page(page: Page):
    page.goto(URL)
    expect(page).to_have_title("Testomat.io")
