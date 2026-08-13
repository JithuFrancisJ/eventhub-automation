from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutPage(BasePage):

    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.decrease_ticket = self.page.locator("#ticket-count").locator("xpath=preceding-sibling::button")
        self.increase_ticket = self.page.locator("#ticket-count").locator("xpath=following-sibling::button")
        self.name = self.page.locator("#customerName")
        self.email = self.page.locator("#customer-email")
        self.phone = self.page.locator("#phone")
        self.total_amount = self.page.locator(".text-indigo-700")
        self.confirm_booking = self.page.locator("#confirm-booking")

    def fill_details(self, name, email, phone):
        self.name.fill(name)
        self.email.fill(email)
        self.phone.fill(phone)

    def increase_tickets(self, count):
        for i in range(count):
            self.increase_ticket.click()

    def decrease_tickets(self, count):
        for i in range(count):
            self.decrease_ticket.click()

    def click_confirm_booking(self):
        self.confirm_booking.click()


