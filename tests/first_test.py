from faker import Faker
from playwright.sync_api import expect

from src.web.Application import Application
from tests.conftest import Configs

target_project = "Popopo"


def test_open_home_page_and_login(login, app: Application):
    """Verifies that the user can open home page and successfully log in."""
    app.projects_page.is_loaded()


def test_open_home_page_and_login_with_invalid_credentials(app: Application, configs: Configs):
    """Verifies login fails when using incorrect credentials."""
    password = Faker().password(length=10)
    print(f"Generated random password: {password}")

    (app.login_page
     .open()
     .is_loaded()
     .login(configs.email, password)
     .invalid_login_message_visible())


def test_search_project(login, app: Application):
    """Verifies project searching functionality."""
    (app.projects_page
     .is_loaded()
     .search_project(target_project)
     .result_project(target_project))


def test_open_free_project(login, app: Application):
    """Verifies project presence under specific workspace options."""
    app.projects_page.is_loaded()

    # Select the company option manually on the projects page
    app.projects_page.page.locator("#company_id").select_option("Free Projects")

    (app.projects_page
     .search_project(target_project))

    expect(app.projects_page.page.get_by_role("heading", name=target_project)).to_be_hidden()
    expect(app.projects_page.page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)
