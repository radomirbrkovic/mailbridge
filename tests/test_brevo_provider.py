import pytest
from mailbridge.providers.brevo_provider import BrevoProvider

@pytest.fixture
def brevo_provider():
    return BrevoProvider(api_key="BREVO.KEY", endpoint="https://api.brevo.com/v3/smtp/email")

def test_send_email_brevo(mocker, brevo_provider):
    mock_post = mocker.patch("requests.post")
    mock_response = mocker.Mock(status_code=201)
    mock_post.return_value = mock_response

    result = brevo_provider.send("to@test.com", "Hi", "<p>Brevo body</p>", "from@test.com")

    assert result is True
    mock_post.assert_called_once_with(
        "https://api.brevo.com/v3/smtp/email",
        json=mocker.ANY,
        headers=mocker.ANY
    )
