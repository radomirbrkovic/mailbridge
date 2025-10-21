import pytest
from mailbridge.providers.smtp_provider import SMTPProvider

@pytest.fixture
def smtp_provider():
    return SMTPProvider(
        host="smtp.test.com",
        port=587,
        username="user@test.com",
        password="secret",
        use_tls=True,
    )

def test_send_email_smtp(mocker, smtp_provider):
    mock_smtp = mocker.patch("smtplib.SMTP", autospec=True)
    instance = mock_smtp.return_value.__enter__.return_value

    result = smtp_provider.send(
        to="receiver@test.com",
        subject="Test Subject",
        body="<b>Hello SMTP</b>",
        from_email="sender@test.com"
    )

    assert result is True
    instance.send_message.assert_called_once()
    instance.login.assert_called_once_with("user@test.com", "secret")