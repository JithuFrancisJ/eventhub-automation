import pytest
from pages.login_page import LoginPage

@pytest.fixture
def authenticated_page(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], config["password"])
    page.wait_for_url(config["base_url"] + "/")
    yield page
