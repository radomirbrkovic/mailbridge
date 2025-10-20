import requests
from .provider_interface import ProviderInterface

class MailgunProvider(ProviderInterface):
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint

    def send(self, to, subject, body, from_email=None):
        data = {
            "from": from_email,
            "to": [to],
            "subject": subject,
            "html": body,
        }

        resp = requests.post(
            self.endpoint,
            auth=("api", self.api_key),
            data=data,
        )
        resp.raise_for_status()
        return resp.status_code == 200