from api.clients.base_client import BaseClient
from api.endpoints.event_endpoints import EventEndpoints

class EventClient(BaseClient):

    def get_events(self, params=None):
        return self.get(EventEndpoints.EVENTS, params=params)

    def get_event(self, event_id):
        return self.get(EventEndpoints.EVENT_BY_ID.format(id=event_id))

    def create_event(self, payload):
        return self.post(EventEndpoints.EVENTS, payload)

    def update_event(self, event_id, payload):
        return self.put(EventEndpoints.EVENT_BY_ID.format(id=event_id), payload)

    def delete_event(self, event_id):
        return self.delete(EventEndpoints.EVENT_BY_ID.format(id=event_id))
