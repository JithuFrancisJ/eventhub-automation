import pytest
from pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.positive
def test_valid_login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], config["password"])
    page.wait_for_url(config["base_url"] + config["urls"]["home"])
    assert page.url == config["base_url"] + config["urls"]["home"]
