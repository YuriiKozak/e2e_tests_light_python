import pytest
from faker import Faker

from src.web.application import Application
from src.web.components.sidebar_tab_enum import SidebarTab


@pytest.mark.regression
def test_new_project_creation(login, app: Application):
    project_title = Faker().company()

    (
        app.new_project_page.open()
        .is_loaded()
        .fill_project_title(project_title)
        .click_create()
    )

    (
        app.project_page.is_loaded()
        .project_title_is(project_title)
        .close_read_me()
        .side_bar.is_loaded()
        .open()
        .navigate_to(SidebarTab.REQUIREMENTS)
        .is_tab_active(SidebarTab.REQUIREMENTS)
        .navigate_to(SidebarTab.TESTS)
        .is_tab_active(SidebarTab.TESTS)
        .close()
    )
