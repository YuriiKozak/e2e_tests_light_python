from playwright.sync_api import Page, expect

from src.web.pages.ProjectsPage import ProjectsPage


def test_search_and_open_project(page: Page, login):
    projects_page = ProjectsPage(page)

    # 1. Open the page and verify that it has loaded successfully
    projects_page.navigate("https://app.testomat.io/projects")
    expect(projects_page.page_indicator).to_be_visible()

    # 2. Verify the subscription plan
    expect(projects_page.header.plan_badge).to_have_text("Enterprise plan")

    # 3. Search for a specific project
    target_title = "Popopo"
    projects_page.header.search(target_title)

    # 4. Get the filtered projects and verify only 1 correct project card is visible
    visible_projects = projects_page.get_all_projects()
    expect(projects_page.project_items).to_have_count(18)

    # Verify card component details
    expect(visible_projects[0].title_locator).to_have_text(target_title)
    expect(visible_projects[0].badge_locator).to_have_text("Classical")

    # 5. Get the specific project by title and click it
    project_card = projects_page.get_project_by_title(target_title)
    project_card.click()
