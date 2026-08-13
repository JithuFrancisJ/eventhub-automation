from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.emailLocator = self.page.get_by_placeholder("you@email.com")
        self.passwordLocator = self.page.locator("input#password")
        self.signInLocator = self.page.get_by_role("button", name="Sign In")
        self.error_invalid_credentials = self.page.locator(".fixed.top-4.right-4 p")
        self.error_invalid_email = self.page.get_by_text("Enter a valid email")
        self.error_invalid_password = self.page.get_by_text(
            "Password must be at least 6 characters"
        )

    def login(self, email, password):
        self.navigate("login")
        self.emailLocator.fill(email)
        self.passwordLocator.fill(password)
        self.signInLocator.click()
