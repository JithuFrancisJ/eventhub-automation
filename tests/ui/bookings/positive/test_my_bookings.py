import pytest
import requests
from pages.login_page import LoginPage
from pages.my_bookings_page import MyBookingsPage
from playwright.sync_api import expect


@pytest.fixture(autouse=True)
def login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], config["password"])
    page.wait_for_url(config["base_url"] + "/")


@pytest.fixture
def booking(config, auth_token):
    h = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
    resp = requests.post(
        config["api_base_url"] + "/bookings",
        json={"eventId": 2, "customerName": "Jithu Francis J", "customerEmail": "jithu@test.com",
              "customerPhone": "9102837465", "quantity": 1},
        headers=h
    )
    data = resp.json()["data"]
    yield data
    requests.delete(config["api_base_url"] + f"/bookings/{data['id']}", headers=h)


@pytest.mark.ui
@pytest.mark.positive
def test_booking_card_displayed(page, config, booking):
    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    expect(bookings_page.booking_cards).to_have_count(1)
    expect(bookings_page.event_name).to_contain_text("Hollywood Monsoon Night")
    expect(bookings_page.total_amount).to_contain_text("$2,500")


@pytest.mark.ui
@pytest.mark.positive
def test_booking_ref_shown_on_card(page, config, booking):
    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    expect(bookings_page.booking_ref.first).to_have_text(booking["bookingRef"])


@pytest.mark.ui
@pytest.mark.positive
def test_view_details_navigates_to_detail_page(page, config, booking):
    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    bookings_page.click_view_details()
    page.wait_for_url(f"**/bookings/{booking['id']}")
    expect(page).to_have_url(config["base_url"] + f"/bookings/{booking['id']}")


@pytest.mark.ui
@pytest.mark.positive
def test_cancel_booking_removes_card(page, config, booking):
    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    bookings_page.click_cancel_booking()
    page.wait_for_timeout(2000)
    expect(bookings_page.booking_cards).to_have_count(0)
    expect(bookings_page.no_bookings).to_be_visible()


@pytest.mark.ui
@pytest.mark.positive
def test_clear_all_bookings(page, config, auth_token):
    h = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
    for _ in range(2):
        requests.post(config["api_base_url"] + "/bookings",
            json={"eventId": 2, "customerName": "Jithu Francis J", "customerEmail": "jithu@test.com",
                  "customerPhone": "9102837465", "quantity": 1}, headers=h)

    page.goto(config["base_url"] + config["urls"]["my_bookings"])
    page.wait_for_timeout(2000)
    bookings_page = MyBookingsPage(page, config)
    expect(bookings_page.booking_cards).to_have_count(2)
    bookings_page.click_clear_all_bookings()
    page.wait_for_timeout(2000)
    expect(bookings_page.booking_cards).to_have_count(0)
    expect(bookings_page.no_bookings).to_be_visible()
