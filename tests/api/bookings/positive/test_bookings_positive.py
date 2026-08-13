import pytest
from utils.assertions import assert_status_code, assert_key_in_response
from utils.test_data import make_booking_payload
from api.models.booking_model import BookingModel


@pytest.fixture
def booking(booking_client):
    resp = booking_client.create_booking(make_booking_payload())
    data = resp.json()["data"]
    yield data
    booking_client.delete_booking(data["id"])


@pytest.mark.api
@pytest.mark.positive
def test_create_booking(booking_client):
    response = booking_client.create_booking(make_booking_payload())
    assert_status_code(response, 201)
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "confirmed"
    assert_key_in_response(data["data"], "bookingRef")
    booking_client.delete_booking(data["data"]["id"])


@pytest.mark.api
@pytest.mark.positive
def test_get_all_bookings(booking_client, booking):
    response = booking_client.get_bookings()
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert_key_in_response(data, "pagination")


@pytest.mark.api
@pytest.mark.positive
def test_get_booking_by_id(booking_client, booking):
    response = booking_client.get_booking(booking["id"])
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == booking["id"]
    assert data["data"]["bookingRef"] == booking["bookingRef"]


@pytest.mark.api
@pytest.mark.positive
def test_get_booking_by_ref(booking_client, booking):
    response = booking_client.get_booking_by_ref(booking["bookingRef"])
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["data"]["bookingRef"] == booking["bookingRef"]


@pytest.mark.api
@pytest.mark.positive
def test_delete_booking(booking_client):
    created = booking_client.create_booking(make_booking_payload()).json()["data"]
    response = booking_client.delete_booking(created["id"])
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Booking cancelled"


@pytest.mark.api
@pytest.mark.positive
def test_create_booking_response_fields(booking_client):
    response = booking_client.create_booking(make_booking_payload())
    assert_status_code(response, 201)
    data = response.json()["data"]
    for field in ["id", "eventId", "customerName", "customerEmail", "customerPhone",
                  "quantity", "totalPrice", "status", "bookingRef"]:
        assert field in data, f"Missing field: {field}"
    booking_client.delete_booking(data["id"])
