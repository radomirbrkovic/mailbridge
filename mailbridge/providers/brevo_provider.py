import requests
from .provider_interface import ProviderInterface

class BrevoProvider(ProviderInterface):
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint

    def send(self, to, subject, body, from_email=None):
        data = {
            "sender": {"email": from_email},
            "to": [{"email": to}],
            "subject": subject,
            "htmlContent": body,
        }

        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        resp = requests.post(self.endpoint, json=data, headers=headers)
        resp.raise_for_status()
        return resp.status_code in (200, 201, 202)