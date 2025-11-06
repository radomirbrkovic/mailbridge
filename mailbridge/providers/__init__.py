"""Email providers."""

from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.providers.brevo_provider import BrevoProvider
from mailbridge.providers.mailgun_provider import MailgunProvider
from mailbridge.providers.postmark_provider import PostmarkProvider
from mailbridge.providers.sendgrid_provider import SendGridProvider
from mailbridge.providers.ses_provider import SESProvider
from mailbridge.providers.smtp_provider import SMTPProvider

__all__ = [
    'EmailMessageDto',
    'BaseEmailProvider',
    'BrevoProvider',
    'MailgunProvider',
    'PostmarkProvider',
    'SendGridProvider',
    'SESProvider',
    'SMTPProvider',
]