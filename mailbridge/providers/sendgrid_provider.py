import requests
from .provider_interface import ProviderInterface

class SendGridProvider(ProviderInterface):
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint

    def send(self, to:str, subject: str, body: str, from_email: str = None):
        data = {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": from_email},
            "subject": subject,
            "content": [{"type": "text/html", "value": body}],
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(self.endpoint, json=data, headers=headers)
        resp.raise_for_status()
        return resp.status_code == 202