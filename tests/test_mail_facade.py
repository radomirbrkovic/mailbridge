import pytest
from unittest.mock import MagicMock, patch
from mailbridge.mail import Mail


@patch("mailbridge.mailer_factory.MailerFactory.get_provider")
def test_mail_send_success(mock_get_provider):
    """Test that Mail.send() calls the provider's send() method correctly."""
    mock_provider = MagicMock()
    mock_provider.send.return_value = True
    mock_get_provider.return_value = mock_provider

    result = Mail.send(
        to="user@example.com",
        subject="Welcome",
        body="<h1>Hello!</h1>",
        from_email="noreply@example.com",
    )

    # Verify result and interactions
    assert result is True
    mock_provider.send.assert_called_once_with(
        to="user@example.com",
        subject="Welcome",
        body="<h1>Hello!</h1>",
        from_email="noreply@example.com",
    )