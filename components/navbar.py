from playwright.sync_api import Page

class NavBar:

    def __init__(self, page: Page):
        self.page = page
        self.homeLink = self.page.locator("#nav-home")
        self.eventsLink = self.page.locator("#nav-events")
        self.myBookingsLink = self.page.locator("#nav-bookings")
        self.logoutBtn = self.page.locator("#logout-btn")