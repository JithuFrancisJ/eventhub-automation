from playwright.sync_api import Page
from pages.base_page import BasePage

class MyBookingsPage(BasePage):

    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.heading = self.page.get_by_text("My Bookings")
        self.sub_heading = self.page.get_by_text("View and manage all your ticket bookings")
        self.clear_all_bookings = self.page.get_by_text("Clear all bookings")
        self.booking_cards = self.page.locator("[data-testid='booking-card']")
        self.booking_ref = self.page.locator(".booking-ref")
        self.event_name = self.page.locator("h3.font-semibold.text-gray-900")
        self.total_amount = self.page.locator("p.text-xl.font-bold.text-indigo-700")
        self.view_details = self.page.get_by_role("button", name="View Details")
        self.cancel_booking = self.page.locator("#cancel-booking-btn")
        self.no_bookings = self.page.get_by_text("No bookings yet")
        self.browse_events = self.page.locator("main").get_by_role("link", name="Browse Events")


    def click_view_details(self, index=0):
        self.view_details.nth(index).click()

    def click_cancel_booking(self, index=0):
        self.cancel_booking.nth(index).click()
        self.page.get_by_role("button", name="Yes, cancel it").click()

    def click_clear_all_bookings(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.clear_all_bookings.click()

