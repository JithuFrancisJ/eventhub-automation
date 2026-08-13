import pytest
from api.clients.auth_client import AuthClient
from api.clients.event_client import EventClient
from api.clients.booking_client import BookingClient

@pytest.fixture(scope="session")
def auth_client(config):
    return AuthClient(base_url=config["api_base_url"])

@pytest.fixture(scope="session")
def auth_token(auth_client, config):
    response = auth_client.login(config["email"], config["password"])
    return response.json().get("token")

@pytest.fixture(scope="session")
def event_client(config, auth_token):
    return EventClient(base_url=config["api_base_url"],
                       headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"})

@pytest.fixture(scope="session")
def booking_client(config, auth_token):
    return BookingClient(base_url=config["api_base_url"],
                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"})
