import pytest
from mailbridge.providers.ses_provider import SESProvider

@pytest.fixture
def ses_provider(mocker):
    mock_client = mocker.Mock()
    mock_client.send_email.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    mock_boto3 = mocker.patch("boto3.client", return_value=mock_client)
    provider = SESProvider("AKIAXXX", "SECRET", "us-east-1")

    return provider

def test_send_email_ses(ses_provider):
    result = ses_provider.send("to@test.com", "Subject", "<p>Body</p>", "from@test.com")

    assert result is True
