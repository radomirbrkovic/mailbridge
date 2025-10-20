import requests
from .provider_interface import ProviderInterface

class PostmarkProvider(ProviderInterface):
    def __init__(self, server_token, endpoint):
        self.server_token = server_token
        self.endpoint = endpoint

    def send(self, to, subject, body, from_email=None):
        data = {
            "From": from_email,
            "To": to,
            "Subject": subject,
            "HtmlBody": body,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": self.server_token,
        }

        resp = requests.post(self.endpoint, json=data, headers=headers)
        resp.raise_for_status()
        return resp.status_code == 200