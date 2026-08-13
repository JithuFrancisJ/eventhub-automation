import json
import os

from api.models.booking_model import BookingModel

BOOKING_DETAILS = {
    "name": "Jithu Francis J",
    "email": "jithu@test.com",
    "phone": "9102837465"
}

INVALID_USER = {
    "email": "wrong@test.com",
    "password": "wrongpassword"
}

def make_booking_payload(event_id=2, quantity=1):
    return BookingModel(
        event_id=event_id,
        customer_name=BOOKING_DETAILS["name"],
        customer_email=BOOKING_DETAILS["email"],
        customer_phone=BOOKING_DETAILS["phone"],
        quantity=quantity
    ).to_dict()

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(path) as f:
        return json.load(f)
