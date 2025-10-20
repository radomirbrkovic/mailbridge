import boto3
from .provider_interface import ProviderInterface

class SESProvider(ProviderInterface):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.client = boto3.client(
            "ses",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def send(self, to, subject, body, from_email=None):
        resp = self.client.send_email(
            Source=from_email,
            Destination={"ToAddresses": [to]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Html": {"Data": body}},
            },
        )
        return resp["ResponseMetadata"]["HTTPStatusCode"] == 200