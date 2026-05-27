from faker import Faker
from playwright.sync_api import Page

from src.web.pages.NewProjectPage import NewProjectPage
from src.web.pages.ProjectPage import ProjectPage


def test_new_project_creation(page: Page, login):
    project_title = Faker().company()

    (NewProjectPage(page)
     .open()
     .is_loaded()
     .fill_project_title(project_title)
     .click_create())

    (ProjectPage(page)
     .is_loaded()
     .project_title_is(project_title)
     .close_read_me())
