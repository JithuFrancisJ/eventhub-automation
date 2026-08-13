import pytest
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage
from api.clients.booking_client import BookingClient
from utils.test_data import BOOKING_DETAILS
from playwright.sync_api import expect


@pytest.fixture(autouse=True)
def login(page, config):
    login_page = LoginPage(page, config)
    login_page.login(config["email"], config["password"])
    page.wait_for_url(config["base_url"] + "/")


@pytest.fixture
def cleanup_booking(config, auth_token):
    created_refs = []
    yield created_refs
    client = BookingClient(
        base_url=config["api_base_url"],
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"}
    )
    for ref in created_refs:
        resp = client.get_booking_by_ref(ref)
        if resp.status_code == 200:
            client.delete_booking(resp.json()["data"]["id"])


def _book_event(page, config, event_path, extra_tickets=0):
    page.goto(config["base_url"] + event_path)
    page.wait_for_timeout(2000)
    checkout = CheckoutPage(page, config)
    if extra_tickets:
        checkout.increase_tickets(extra_tickets)
    checkout.fill_details(BOOKING_DETAILS["name"], BOOKING_DETAILS["email"], BOOKING_DETAILS["phone"])
    checkout.click_confirm_booking()
    page.wait_for_timeout(2000)
    return OrderConfirmationPage(page, config)


@pytest.mark.ui
@pytest.mark.positive
def test_book_single_ticket(page, config, cleanup_booking):
    confirmation = _book_event(page, config, "/events/2")
    expect(confirmation.booking_confirmed_msg).to_be_visible()
    expect(confirmation.customer_name).to_have_text(BOOKING_DETAILS["name"])
    expect(confirmation.tickets).to_have_text("1")
    expect(confirmation.total).to_have_text("$2,500")
    cleanup_booking.append(confirmation.booking_ref.inner_text())


@pytest.mark.ui
@pytest.mark.positive
def test_book_multiple_tickets(page, config, cleanup_booking):
    confirmation = _book_event(page, config, "/events/2", extra_tickets=2)
    expect(confirmation.booking_confirmed_msg).to_be_visible()
    expect(confirmation.tickets).to_have_text("3")
    expect(confirmation.total).to_have_text("$7,500")
    cleanup_booking.append(confirmation.booking_ref.inner_text())


@pytest.mark.ui
@pytest.mark.positive
def test_booking_ref_is_displayed(page, config, cleanup_booking):
    confirmation = _book_event(page, config, "/events/2")
    expect(confirmation.booking_confirmed_msg).to_be_visible()
    expect(confirmation.booking_ref).not_to_be_empty()
    cleanup_booking.append(confirmation.booking_ref.inner_text())


@pytest.mark.ui
@pytest.mark.positive
def test_view_my_bookings_after_booking(page, config, cleanup_booking):
    confirmation = _book_event(page, config, "/events/2")
    expect(confirmation.booking_confirmed_msg).to_be_visible()
    cleanup_booking.append(confirmation.booking_ref.inner_text())
    confirmation.click_view_my_bookings()
    page.wait_for_url(config["base_url"] + config["urls"]["my_bookings"])
    expect(page).to_have_url(config["base_url"] + config["urls"]["my_bookings"])


@pytest.mark.ui
@pytest.mark.positive
def test_browse_more_events_after_booking(page, config, cleanup_booking):
    confirmation = _book_event(page, config, "/events/2")
    expect(confirmation.booking_confirmed_msg).to_be_visible()
    cleanup_booking.append(confirmation.booking_ref.inner_text())
    confirmation.click_browse_more_events()
    page.wait_for_url(config["base_url"] + config["urls"]["events"])
    expect(page).to_have_url(config["base_url"] + config["urls"]["events"])
