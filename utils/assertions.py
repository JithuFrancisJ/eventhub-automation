def assert_status_code(response, expected_code):
    assert response.status_code == expected_code, \
        f"Expected {expected_code}, got {response.status_code}"

def assert_key_in_response(response_json, key):
    assert key in response_json, f"Key '{key}' not found in response"

def get_detail_message(response, field):
    return next(d["message"] for d in response.json()["details"] if d["field"] == field)
