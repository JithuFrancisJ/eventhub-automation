from dataclasses import dataclass

@dataclass
class EventModel:
    title: str
    category: str
    venue: str
    city: str
    event_date: str
    price: float
    total_seats: int
    description: str = ""
    image_url: str = ""

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "venue": self.venue,
            "city": self.city,
            "eventDate": self.event_date,
            "price": self.price,
            "totalSeats": self.total_seats,
            "imageUrl": self.image_url
        }
