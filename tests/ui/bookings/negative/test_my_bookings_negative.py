import pytest
from pages.login_page import LoginPage
from pages.my_bookings_page import MyBookingsPage
from playwright.sync_api import expect


@pytest.fixture(autouse=True)
def login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], config["password"])
    page.wait_for_url(config["base_url"] + "/")


@pytest.mark.ui
@pytest.mark.negative
def test_no_bookings_shows_empty_state(page, config):
    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    expect(bookings_page.booking_cards).to_have_count(0)
    expect(bookings_page.no_bookings).to_be_visible()


@pytest.mark.ui
@pytest.mark.negative
def test_empty_state_browse_events_navigates(page, config):
    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    expect(bookings_page.no_bookings).to_be_visible()
    bookings_page.browse_events.click()
    page.wait_for_url(config["base_url"] + config["urls"]["events"])
    expect(page).to_have_url(config["base_url"] + config["urls"]["events"])
