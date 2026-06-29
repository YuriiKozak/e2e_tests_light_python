from typing import Self

import allure
from playwright.sync_api import Page, expect


class NewProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.__form_container = page.locator("#content-desktop .new_project")

    @allure.step("Open New Project Page")
    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    @allure.step("Verify New Project Page is loaded")
    def is_loaded(self) -> Self:
        expect(self.__form_container).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_be_visible()
        expect(self.__form_container.locator("#classical")).to_contain_text("Classical")
        expect(self.__form_container.locator("#bdd")).to_be_visible()
        expect(self.__form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self.__form_container.locator("#project_title")).to_be_visible()
        expect(self.__form_container.locator("#demo-btn")).to_be_visible()
        expect(self.__form_container.locator("#project-create-btn")).to_be_visible()
        return self

    @allure.step("Fill project title: {target_project_title}")
    def fill_project_title(self, target_project_title: str) -> Self:
        self.__form_container.locator("#project_title").fill(target_project_title)
        return self

    @allure.step("Click 'Create' button")
    def click_create(self) -> Self:
        self.__form_container.locator("#project-create-btn input").click()
        expect(self.__form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
        return self
