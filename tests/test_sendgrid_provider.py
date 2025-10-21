import pytest
from mailbridge.providers.sendgrid_provider import SendGridProvider

@pytest.fixture
def sendgrid_provider():
    return SendGridProvider(
        api_key="SG.TESTKEY",
        endpoint="https://api.sendgrid.com/v3/mail/send"
    )

def test_send_email_sendgrid(mocker, sendgrid_provider):
    mock_post = mocker.patch("requests.post")
    mock_response = mocker.Mock(status_code=202)
    mock_post.return_value = mock_response

    result = sendgrid_provider.send("to@test.com", "Hello", "<p>Body</p>", "from@test.com")

    assert result is True
    mock_post.assert_called_once_with(
        "https://api.sendgrid.com/v3/mail/send",
        json=mocker.ANY,
        headers=mocker.ANY
    )