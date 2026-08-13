import pytest
from utils.assertions import assert_status_code, assert_key_in_response, get_detail_message
from utils.test_data import INVALID_USER


@pytest.mark.api
@pytest.mark.negative
def test_invalid_credentials_login(auth_client, config):
    response = auth_client.login(INVALID_USER["email"], "password")
    assert_status_code(response, 400)
    assert response.json()["error"] == "Invalid email or password"

@pytest.mark.api
@pytest.mark.negative
def test_invalid_email_login(auth_client, config):
    response = auth_client.login(INVALID_USER["email"], config["password"])
    assert_status_code(response, 400)
    assert response.json()["error"] == "Invalid email or password"

@pytest.mark.api
@pytest.mark.negative
def test_invalid_password_login(auth_client, config):
    response = auth_client.login(config["email"], "password")
    assert_status_code(response, 400)
    assert response.json()["error"] == "Invalid email or password"

@pytest.mark.api
@pytest.mark.negative
def test_null_email_login(auth_client, config):
    response = auth_client.login("", config["password"])
    assert_status_code(response, 400)
    assert get_detail_message(response, "email") == "A valid email is required"

@pytest.mark.api
@pytest.mark.negative
def test_null_password_login(auth_client, config):
    response = auth_client.login(config["email"], "")
    assert_status_code(response, 400)
    assert get_detail_message(response, "password") == "Password must be at least 6 characters"

@pytest.mark.api
@pytest.mark.negative
def test_null_credentials_login(auth_client, config):
    response = auth_client.login("", "")
    assert_status_code(response, 400)
    assert get_detail_message(response, "email") == "A valid email is required"
    assert get_detail_message(response, "password") == "Password must be at least 6 characters"

@pytest.mark.api
@pytest.mark.negative
def test_get_me_invalid_token(auth_client):
    response = auth_client.get_me("invalidtoken123")
    assert_status_code(response, 401)
    assert response.json()["error"] == "Invalid or expired token"