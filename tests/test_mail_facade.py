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

@patch("mailbridge.mailer_factory.MailerFactory.get_provider")
def test_mail_send_failure(mock_get_provider):
    """Test that Mail.send() returns False if provider.send() raises an error."""
    mock_provider = MagicMock()
    mock_provider.send.side_effect = Exception("Something went wrong")
    mock_get_provider.return_value = mock_provider

    result = Mail.send(
        to="user@example.com",
        subject="Fail Test",
        body="Error expected",
        from_email="noreply@example.com",
    )

    assert result is False
    mock_provider.send.assert_called_once()

@patch("mailbridge.mailer_factory.MailerFactory.get_provider")
def test_mail_send_without_from_email(mock_get_provider):
    """Ensure Mail.send works even if from_email is omitted."""
    mock_provider = MagicMock()
    mock_provider.send.return_value = True
    mock_get_provider.return_value = mock_provider

    result = Mail.send(
        to="user@example.com",
        subject="No sender",
        body="Testing no from_email",
    )

    assert result is True
    mock_provider.send.assert_called_once_with(
        to="user@example.com",
        subject="No sender",
        body="Testing no from_email",
        from_email=None,
    )