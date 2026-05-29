import pytest
from playwright.sync_api import expect

from src.web.application import Application

target_project = "Popopo"


@pytest.mark.regression
def test_project_search(login, app: Application):
    (
        app.projects_page.is_loaded()
        .search_project(target_project)
        .result_project(target_project)
    )


@pytest.mark.regression
def test_open_free_project(login, app: Application):
    (
        app.projects_page.is_loaded()
        .select_project("Free Projects")
        .search_project(target_project)
    )

    expect(
        app.projects_page.page.get_by_role("heading", name=target_project)
    ).to_be_hidden()
    expect(
        app.projects_page.page.get_by_text("You have not created any projects yet")
    ).to_be_visible(timeout=10000)
