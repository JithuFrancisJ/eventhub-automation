import pytest
from utils.assertions import assert_status_code, assert_key_in_response


@pytest.mark.api
@pytest.mark.positive
def test_get_all_events(event_client):
    response = event_client.get_events()
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 3
    assert_key_in_response(data, "pagination")


@pytest.mark.api
@pytest.mark.positive
def test_get_event_by_id(event_client):
    response = event_client.get_event(1)
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["title"] == "World Tech Summit"
    assert data["data"]["category"] == "Conference"


@pytest.mark.api
@pytest.mark.positive
def test_get_events_response_fields(event_client):
    response = event_client.get_events()
    assert_status_code(response, 200)
    event = response.json()["data"][0]
    for field in ["id", "title", "category", "venue", "city", "price", "availableSeats", "totalSeats"]:
        assert field in event, f"Missing field: {field}"


@pytest.mark.api
@pytest.mark.positive
def test_search_events_by_keyword(event_client):
    response = event_client.get_events(params={"search": "Tech"})
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    titles = [e["title"] for e in data["data"]]
    assert any("Tech" in t for t in titles)


@pytest.mark.api
@pytest.mark.positive
def test_filter_events_by_category(event_client):
    response = event_client.get_events(params={"category": "Concert"})
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["category"] == "Concert"


@pytest.mark.api
@pytest.mark.positive
def test_filter_events_by_city(event_client):
    response = event_client.get_events(params={"city": "Delhi"})
    assert_status_code(response, 200)
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["city"] == "Delhi"
