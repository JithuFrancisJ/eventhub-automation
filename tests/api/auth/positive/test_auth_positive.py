import pytest
from utils.assertions import assert_status_code, assert_key_in_response
import uuid
import os


@pytest.mark.api
@pytest.mark.positive
def test_valid_login(auth_client, config):
    response = auth_client.login(config["email"], config["password"])
    assert_status_code(response, 200)
    assert_key_in_response(response.json(), "token")


@pytest.mark.api
@pytest.mark.positive
def test_register(auth_client):
    random_email = f"testuser_{uuid.uuid4().hex[:8]}@test.com"
    password = "Test@123"
    response = auth_client.register(random_email, password)
    assert_status_code(response, 201)
    assert_key_in_response(response.json(), "token")

    path = os.path.join("data", "registered_users.txt")
    with open(path, "a") as f:
        f.write(f"{random_email},{password}\n")


@pytest.mark.api
@pytest.mark.positive
def test_get_me(auth_client, auth_token):
    response = auth_client.get_me(auth_token)
    assert_status_code(response, 200)
    assert_key_in_response(response.json(), "user")
