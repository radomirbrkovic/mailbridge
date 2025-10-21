import os
import pytest
from mailbridge.mailer_factory import MailerFactory
from mailbridge.providers.smtp_provider import SMTPProvider
from mailbridge.providers.sendgrid_provider import SendGridProvider
from mailbridge.providers.mailgun_provider import MailgunProvider
from mailbridge.providers.ses_provider import SESProvider
from mailbridge.providers.postmark_provider import PostmarkProvider
from mailbridge.providers.brevo_provider import BrevoProvider


@pytest.mark.parametrize(
    "provider_name,expected_class,env_vars",
    [
        (
            "smtp",
            SMTPProvider,
            {
                "MAIL_MAILER": "smtp",
                "MAIL_HOST": "smtp.test.com",
                "MAIL_PORT": "587",
                "MAIL_USERNAME": "user@test.com",
                "MAIL_PASSWORD": "secret",
                "MAIL_ENCRYPTION": "True",
            },
        ),
        (
            "sendgrid",
            SendGridProvider,
            {
                "MAIL_MAILER": "sendgrid",
                "MAIL_API_KEY": "SG.KEY",
                "MAIL_ENDPOINT": "https://api.sendgrid.com/v3/mail/send",
            },
        ),
        (
            "mailgun",
            MailgunProvider,
            {
                "MAIL_MAILER": "mailgun",
                "MAIL_API_KEY": "MG.KEY",
                "MAIL_ENDPOINT": "https://api.mailgun.net/v3/test/messages",
            },
        ),
        (
            "ses",
            SESProvider,
            {
                "MAIL_MAILER": "ses",
                "MAIL_AWS_ACCESS_KEY_ID": "AKIAXXX",
                "MAIL_AWS_SECRET_ACCESS_KEY": "SECRET",
                "MAIL_AWS_REGION": "us-east-1",
            },
        ),
        (
            "postmark",
            PostmarkProvider,
            {
                "MAIL_MAILER": "postmark",
                "MAIL_API_KEY": "PM.KEY",
                "MAIL_ENDPOINT": "https://api.postmarkapp.com/email",
            },
        ),
        (
            "brevo",
            BrevoProvider,
            {
                "MAIL_MAILER": "brevo",
                "MAIL_API_KEY": "BREVO.KEY",
                "MAIL_ENDPOINT": "https://api.brevo.com/v3/smtp/email",
            },
        ),
    ],
)
def test_mailer_factory_get_provider(provider_name, expected_class, env_vars, mocker):
    # Save original environment
    original_env = os.environ.copy()

    # Override env vars for test
    os.environ.update(env_vars)

    provider = MailerFactory.get_provider()

    assert isinstance(provider, expected_class), f"{provider_name} did not return expected provider"

    # Restore environment
    os.environ.clear()
    os.environ.update(original_env)


def test_mailer_factory_invalid_provider(monkeypatch):
    monkeypatch.setenv("MAIL_MAILER", "unknown")

    with pytest.raises(ValueError) as exc_info:
        MailerFactory.get_provider()

    assert "Unsupported mail provider" in str(exc_info.value)
