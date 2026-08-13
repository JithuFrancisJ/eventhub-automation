from api.clients.base_client import BaseClient
from api.endpoints.booking_endpoints import BookingEndpoints

class BookingClient(BaseClient):

    def get_bookings(self, params=None):
        return self.get(BookingEndpoints.BOOKINGS, params=params)

    def get_booking(self, booking_id):
        return self.get(BookingEndpoints.BOOKING_BY_ID.format(id=booking_id))

    def get_booking_by_ref(self, ref):
        return self.get(BookingEndpoints.BOOKING_BY_REF.format(ref=ref))

    def create_booking(self, payload):
        return self.post(BookingEndpoints.BOOKINGS, payload)

    def delete_booking(self, booking_id):
        return self.delete(BookingEndpoints.BOOKING_BY_ID.format(id=booking_id))
