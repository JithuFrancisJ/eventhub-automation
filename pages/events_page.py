from playwright.sync_api import Page
from pages.base_page import BasePage

class EventsPage(BasePage):

    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.search = self.page.get_by_placeholder("Search events, venues…")
        self.categories = self.page.get_by_role("combobox").first
        self.cities = self.page.get_by_role("combobox").last
        self.book_now_buttons = self.page.locator("#book-now-btn")
        self.event_links = self.page.locator("article a")
        self.event_titles = self.page.locator("article h3")
        self.event_cards = self.page.locator("article")
        self.no_results = self.page.get_by_text("No events found")
        self.clear_filters = self.page.get_by_text("Clear filters")

    def search_event(self, text):
        self.search.click()
        self.search.fill(text)

    def select_category(self, category):
        self.categories.select_option(category)

    def select_city(self, city):
        self.cities.select_option(city)

    def click_book_now(self, index=0):
        self.book_now_buttons.nth(index).click()

    def click_event_link(self, index=0):
        self.event_links.nth(index).click()
