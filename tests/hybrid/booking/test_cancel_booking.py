# Hybrid - Cancel Booking Test
import pytest
from pages.my_bookings_page import MyBookingsPage
from utils.test_data import make_booking_payload
from utils.assertions import assert_status_code
from playwright.sync_api import expect


@pytest.mark.hybrid
@pytest.mark.positive
def test_cancel_via_ui_verify_via_api(authenticated_page, config, booking_client):
    booking = booking_client.create_booking(make_booking_payload()).json()["data"]

    authenticated_page.goto(config["base_url"] + config["urls"]["my_bookings"])
    authenticated_page.wait_for_timeout(2000)

    bookings_page = MyBookingsPage(authenticated_page, config)
    bookings_page.click_cancel_booking()
    authenticated_page.wait_for_timeout(2000)

    expect(bookings_page.booking_cards).to_have_count(0)

    response = booking_client.get_booking(booking["id"])
    assert_status_code(response, 404)
