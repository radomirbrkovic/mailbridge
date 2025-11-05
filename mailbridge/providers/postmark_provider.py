import base64
from pathlib import Path
from typing import Dict, Any, List
import requests
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.exceptions import ConfigurationError, EmailSendError

class PostmarkProvider(BaseEmailProvider):

    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        pass

    def _validate_config(self) -> None:
        """Validate Postmark configuration."""
        if 'server_token' not in self.config:
            raise ConfigurationError(
                "Missing required Postmark configuration: server_token"
            )

        self.endpoint = self.config.get(
            'endpoint',
            'https://api.postmarkapp.com/email'
        )

    def _build_payload(self, message: EmailMessageDto) -> Dict[str, Any]:
        payload = {
            'From': message.from_email or self.config.get('from_email'),
            'To': ', '.join(message.to),
            'Subject': message.subject,
        }

        if message.html:
            payload['HtmlBody'] = message.body
        else:
            payload['TextBody'] = message.body

        if message.cc:
            payload['Cc'] = ', '.join(message.cc)
        if message.bcc:
            payload['Bcc'] = ', '.join(message.bcc)

        if message.reply_to:
            payload['ReplyTo'] = message.reply_to

        if message.headers:
            payload['Headers'] = [
                {'Name': key, 'Value': value}
                for key, value in message.headers.items()
            ]

        if message.attachments:
            payload['Attachments'] = self._build_attachments(message.attachments)

        if self.config.get('track_opens'):
            payload['TrackOpens'] = True
        if self.config.get('track_links'):
            payload['TrackLinks'] = self.config['track_links']

        return payload