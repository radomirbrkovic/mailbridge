import pytest
from mailbridge.providers.mailgun_provider import MailgunProvider

@pytest.fixture
def mailgun_provider():
    return MailgunProvider(
        api_key="MG.TESTKEY",
        endpoint="https://api.mailgun.net/v3/test/messages"
    )

def test_send_email_mailgun(mocker, mailgun_provider):
    mock_post = mocker.patch("requests.post")
    mock_response = mocker.Mock(status_code=200)
    mock_post.return_value = mock_response

    result = mailgun_provider.send("to@test.com", "Hi", "<p>Mailgun body</p>", "from@test.com")

    assert result is True
    mock_post.assert_called_once_with(
        "https://api.mailgun.net/v3/test/messages",
        auth=("api", "MG.TESTKEY"),
        data=mocker.ANY
    )
