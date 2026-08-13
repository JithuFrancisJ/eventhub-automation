import pytest
from utils.assertions import assert_status_code


@pytest.mark.api
@pytest.mark.negative
def test_get_event_nonexistent_id(event_client):
    response = event_client.get_event(9999)
    assert_status_code(response, 404)
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()


@pytest.mark.api
@pytest.mark.negative
def test_get_event_invalid_id(event_client):
    response = event_client.get_event("abc")
    assert_status_code(response, 500)
    data = response.json()
    assert data["success"] is False


@pytest.mark.api
@pytest.mark.negative
def test_search_events_no_results(event_client):
    response = event_client.get_events(params={"search": "xyznonexistent999"})
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["data"] == []
    assert data["pagination"]["total"] == 0


@pytest.mark.api
@pytest.mark.negative
def test_filter_events_invalid_category(event_client):
    response = event_client.get_events(params={"category": "InvalidCategory"})
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["data"] == []


@pytest.mark.api
@pytest.mark.negative
def test_filter_events_invalid_city(event_client):
    response = event_client.get_events(params={"city": "InvalidCity"})
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["data"] == []
