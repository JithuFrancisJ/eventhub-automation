from api.clients.base_client import BaseClient
from api.endpoints.auth_endpoints import AuthEndpoints

class AuthClient(BaseClient):

    def register(self, email, password):
        return self.post(AuthEndpoints.REGISTER, {"email": email, "password": password})

    def login(self, email, password):
        return self.post(AuthEndpoints.LOGIN, {"email": email, "password": password})

    def get_me(self, token):
        return self.get(AuthEndpoints.ME, headers={"Authorization": f"Bearer {token}"})