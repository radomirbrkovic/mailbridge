import base64
from pathlib import Path
from typing import Dict, Any, List
import requests
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.exceptions import ConfigurationError, EmailSendError

class BrevoProvider(BaseEmailProvider):
    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        pass

    def _validate_config(self) -> None:
        """Validate Brevo configuration."""
        if 'api_key' not in self.config:
            raise ConfigurationError(
                "Missing required Brevo configuration: api_key"
            )

        self.endpoint = self.config.get(
            'endpoint',
            'https://api.brevo.com/v3/smtp/email'
        )

    def _build_payload(self, message: EmailMessageDto) -> Dict[str, Any]:

        payload = {
            'sender': {
                'email': message.from_email or self.config.get('from_email')
            },
            'to': [{'email': email} for email in message.to],
            'subject': message.subject,
        }

        if message.html:
            payload['htmlContent'] = message.body
        else:
            payload['textContent'] = message.body

        if message.cc:
            payload['cc'] = [{'email': email} for email in message.cc]

        if message.bcc:
            payload['bcc'] = [{'email': email} for email in message.bcc]

        if message.reply_to:
            payload['replyTo'] = {'email': message.reply_to}

        if message.headers:
            payload['headers'] = message.headers

        if message.attachments:
            payload['attachment'] = self._build_attachments(message.attachments)

        if self.config.get('tags'):
            payload['tags'] = self.config['tags']

        return payload