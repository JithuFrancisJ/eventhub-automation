from dataclasses import dataclass

@dataclass
class BookingModel:
    event_id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    quantity: int

    def to_dict(self):
        return {
            "eventId": self.event_id,
            "customerName": self.customer_name,
            "customerEmail": self.customer_email,
            "customerPhone": self.customer_phone,
            "quantity": self.quantity
        }
