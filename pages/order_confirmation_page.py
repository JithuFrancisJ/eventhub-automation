from playwright.sync_api import Page
from pages.base_page import BasePage

class OrderConfirmationPage(BasePage):

    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.booking_confirmed_msg = self.page.get_by_text("Booking Confirmed!")
        self.booking_ref = self.page.locator("span.font-medium.text-gray-900").nth(0)
        self.customer_name = self.page.locator("span.font-medium.text-gray-900").nth(1)
        self.tickets = self.page.locator("span.font-medium.text-gray-900").nth(2)
        self.total = self.page.locator("span.font-medium.text-gray-900").nth(3)
        self.view_my_bookings = self.page.get_by_role("button", name="View My Bookings")
        self.browse_more_events = self.page.get_by_role("button", name="Browse More Events")

    def click_view_my_bookings(self):
        self.view_my_bookings.click()

    def click_browse_more_events(self):
        self.browse_more_events.click()


