from playwright.sync_api import Locator


class HeaderComponent:
    def __init__(self, locator: Locator):
        """Component for the top dashboard control panel (.common-page-header)."""
        self.locator = locator

        # Left side elements
        self.title = locator.locator(".common-page-header-left h2")
        self.company_select = locator.locator("#company_id")
        self.plan_badge = locator.locator(".tooltip-project-plan span")

        # Right side elements
        self.search_input = locator.locator("#search")
        self.create_button = locator.locator("a:has-text('Create')")
        self.grid_view_tab = locator.locator("#grid-view")
        self.table_view_tab = locator.locator("#table-view")

    def get_title_text(self) -> str:
        """Returns the main header title text."""
        return self.title.inner_text().strip()

    def select_company(self, company_name: str):
        """Selects a company from the dropdown menu."""
        self.company_select.select_option(label=company_name)

    def get_current_plan(self) -> str:
        """Returns the subscription plan text."""
        return self.plan_badge.inner_text().strip()

    def search(self, query: str):
        """Fills the project search field."""
        self.search_input.fill(query)

    def click_create(self):
        """Clicks the 'Create' project button."""
        self.create_button.click()

    def switch_to_table_view(self):
        """Switches the view to table mode."""
        self.table_view_tab.click()

    def switch_to_grid_view(self):
        """Switches the view to grid mode."""
        self.grid_view_tab.click()
