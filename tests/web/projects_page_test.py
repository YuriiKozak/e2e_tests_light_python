import pytest

from src.web.application import Application

FREE_PROJECTS = "Free Projects"
TARGET_PROJECT = "Popopo"


@pytest.mark.regression
def test_project_search(login, app: Application):
    (
        app.projects_page.is_loaded()
        .search_project(TARGET_PROJECT)
        .result_project(TARGET_PROJECT)
    )


@pytest.mark.regression
def test_open_free_project(login, app: Application):
    (
        app.projects_page.is_loaded()
        .select_project(FREE_PROJECTS)
        .search_project(TARGET_PROJECT)
        .project_is_hidden(TARGET_PROJECT)
        .empty_state_is_visible()
    )
