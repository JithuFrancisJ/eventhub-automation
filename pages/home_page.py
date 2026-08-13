from playwright.sync_api import Page
from pages.base_page import BasePage

class HomePage(BasePage):

    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.browse_events = self.page.get_by_text("Browse Events")
        self.my_bookings = self.page.get_by_role("button", name="My Bookings")
        self.view_all = self.page.get_by_text("View all →")
        self.book_now = self.page.locator("#book-now-btn")
        self.explore_all_events = self.page.get_by_role("button", name="Explore All Events")

    def click_browse_events(self):
        self.browse_events.click()

    def click_my_bookings(self):
        self.my_bookings.click()

    def click_view_all(self):
        self.view_all.click()

    def click_book_now(self):
        self.book_now.click()

    def click_explore_all_events(self):
        self.explore_all_events.click()
    