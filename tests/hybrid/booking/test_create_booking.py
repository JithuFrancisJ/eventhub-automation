# Hybrid - Create Booking Test
import pytest
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage
from utils.test_data import BOOKING_DETAILS
from utils.assertions import assert_status_code


@pytest.mark.hybrid
@pytest.mark.positive
def test_book_via_ui_verify_via_api(authenticated_page, config, booking_client):
    authenticated_page.goto(config["base_url"] + "/events/2")
    authenticated_page.wait_for_timeout(2000)

    checkout = CheckoutPage(authenticated_page, config)
    checkout.fill_details(BOOKING_DETAILS["name"], BOOKING_DETAILS["email"], BOOKING_DETAILS["phone"])
    checkout.click_confirm_booking()
    authenticated_page.wait_for_timeout(2000)

    confirmation = OrderConfirmationPage(authenticated_page, config)
    booking_ref = confirmation.booking_ref.inner_text()

    response = booking_client.get_booking_by_ref(booking_ref)
    assert_status_code(response, 200)
    data = response.json()["data"]
    assert data["bookingRef"] == booking_ref
    assert data["customerName"] == BOOKING_DETAILS["name"]
    assert data["status"] == "confirmed"

    booking_client.delete_booking(data["id"])
