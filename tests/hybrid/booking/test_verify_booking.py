# Hybrid - Verify Booking Test
import pytest
from pages.my_bookings_page import MyBookingsPage
from utils.test_data import make_booking_payload
from playwright.sync_api import expect


@pytest.fixture
def api_booking(booking_client):
    resp = booking_client.create_booking(make_booking_payload())
    data = resp.json()["data"]
    yield data
    booking_client.delete_booking(data["id"])


@pytest.mark.hybrid
@pytest.mark.positive
def test_api_booking_appears_on_ui(authenticated_page, config, api_booking):
    authenticated_page.goto(config["base_url"] + config["urls"]["my_bookings"])
    authenticated_page.wait_for_timeout(2000)

    bookings_page = MyBookingsPage(authenticated_page, config)
    expect(bookings_page.booking_cards).to_have_count(1)
    expect(bookings_page.booking_ref.first).to_have_text(api_booking["bookingRef"])
