import pytest
import requests
from utils.assertions import assert_status_code, get_detail_message
from utils.test_data import BOOKING_DETAILS, make_booking_payload


@pytest.mark.api
@pytest.mark.negative
def test_create_booking_missing_fields(booking_client):
    response = booking_client.create_booking({"eventId": 2})
    assert_status_code(response, 400)
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Validation failed"
    assert get_detail_message(response, "customerName") == "Customer name is required"
    assert get_detail_message(response, "customerEmail") == "Customer email is required"
    assert get_detail_message(response, "customerPhone") == "Customer phone is required"
    assert get_detail_message(response, "quantity") == "Quantity is required"


@pytest.mark.api
@pytest.mark.negative
def test_create_booking_invalid_event_id(booking_client):
    response = booking_client.create_booking(make_booking_payload(event_id=9999))
    assert_status_code(response, 404)
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()


@pytest.mark.api
@pytest.mark.negative
def test_get_booking_nonexistent_id(booking_client):
    response = booking_client.get_booking(9999)
    assert_status_code(response, 404)
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()


@pytest.mark.api
@pytest.mark.negative
def test_get_booking_by_invalid_ref(booking_client):
    response = booking_client.get_booking_by_ref("INVALID")
    assert_status_code(response, 404)
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()


@pytest.mark.api
@pytest.mark.negative
def test_delete_booking_nonexistent_id(booking_client):
    response = booking_client.delete_booking(9999)
    assert_status_code(response, 404)
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()


@pytest.mark.api
@pytest.mark.negative
def test_get_bookings_without_auth(config):
    response = requests.get(config["api_base_url"] + "/bookings")
    assert_status_code(response, 401)
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Unauthorized"
