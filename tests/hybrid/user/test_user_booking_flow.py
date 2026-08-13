# Hybrid - User Booking Flow Test
import pytest
from pages.events_page import EventsPage
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage
from pages.my_bookings_page import MyBookingsPage
from utils.test_data import BOOKING_DETAILS
from utils.assertions import assert_status_code
from playwright.sync_api import expect


@pytest.mark.hybrid
@pytest.mark.positive
def test_full_booking_flow(authenticated_page, config, booking_client):
    # Navigate to events and book
    authenticated_page.goto(config["base_url"] + config["urls"]["events"])
    authenticated_page.wait_for_timeout(2000)

    events_page = EventsPage(authenticated_page, config)
    events_page.search_event("Hollywood")
    authenticated_page.wait_for_timeout(1000)
    events_page.click_book_now()
    authenticated_page.wait_for_url("**/events/**")
    authenticated_page.wait_for_timeout(2000)

    checkout = CheckoutPage(authenticated_page, config)
    checkout.fill_details(BOOKING_DETAILS["name"], BOOKING_DETAILS["email"], BOOKING_DETAILS["phone"])
    checkout.click_confirm_booking()
    authenticated_page.wait_for_timeout(2000)

    confirmation = OrderConfirmationPage(authenticated_page, config)
    expect(confirmation.booking_confirmed_msg).to_be_visible()
    booking_ref = confirmation.booking_ref.inner_text()

    # Verify via API
    api_resp = booking_client.get_booking_by_ref(booking_ref)
    assert_status_code(api_resp, 200)
    assert api_resp.json()["data"]["status"] == "confirmed"

    # Navigate to My Bookings and verify UI
    confirmation.click_view_my_bookings()
    authenticated_page.wait_for_url(config["base_url"] + config["urls"]["my_bookings"])
    bookings_page = MyBookingsPage(authenticated_page, config)
    expect(bookings_page.booking_ref.first).to_have_text(booking_ref)

    # Cleanup
    booking_client.delete_booking(api_resp.json()["data"]["id"])
