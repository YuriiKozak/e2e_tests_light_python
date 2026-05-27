from playwright.sync_api import Page, expect


def test_open_home_page(page: Page):
    page.goto("https://app.testomat.io/")

    expect(page).to_have_title("Testomat.io")
