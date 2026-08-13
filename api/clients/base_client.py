import requests

class BaseClient:

    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "application/json"}

    def get(self, endpoint, params=None, headers=None):
        headers = headers or self.headers
        return requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)

    def post(self, endpoint, payload=None):
        return requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=payload)

    def put(self, endpoint, payload=None):
        return requests.put(f"{self.base_url}{endpoint}", headers=self.headers, json=payload)

    def delete(self, endpoint):
        return requests.delete(f"{self.base_url}{endpoint}", headers=self.headers)
