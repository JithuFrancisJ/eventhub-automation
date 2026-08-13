import pytest
from pages.login_page import LoginPage
from utils.test_data import INVALID_USER
from playwright.sync_api import expect


@pytest.mark.ui
@pytest.mark.negative
def test_invalid_email_valid_password_login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(INVALID_USER["email"], config["password"])
    expect(login_page.error_invalid_credentials).to_have_text(
        "Invalid email or password"
    )


@pytest.mark.ui
@pytest.mark.negative
def test_valid_email_invalid_password_login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], INVALID_USER["password"])
    expect(login_page.error_invalid_credentials).to_have_text(
        "Invalid email or password"
    )


@pytest.mark.ui
@pytest.mark.negative
def test_null_email_null_password_login(page, config):
    login_page = LoginPage(page, config)
    login_page.login("", "")
    expect(login_page.error_invalid_email).to_have_text("Enter a valid email")
    expect(login_page.error_invalid_password).to_have_text(
        "Password must be at least 6 characters"
    )


@pytest.mark.ui
@pytest.mark.negative
def test_null_email_valid_password_login(page, config):
    login_page = LoginPage(page, config)
    login_page.login("", config["password"])
    expect(login_page.error_invalid_email).to_have_text("Enter a valid email")


@pytest.mark.ui
@pytest.mark.negative
def test_valid_email_null_password_login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], "")
    expect(login_page.error_invalid_password).to_have_text(
        "Password must be at least 6 characters"
    )
