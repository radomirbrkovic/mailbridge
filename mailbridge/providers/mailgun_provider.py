import base64
from pathlib import Path
from typing import Dict, Any, List
import requests
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.exceptions import ConfigurationError, EmailSendError

class MailgunProvider(BaseEmailProvider):

    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        pass

    def _validate_config(self) -> None:
        required = ['api_key', 'endpoint']
        missing = [key for key in required if key not in self.config]
        if missing:
            raise ConfigurationError(
                f"Missing required Mailgun configuration: {', '.join(missing)}"
            )

    def _build_from_data(self, message: EmailMessageDto) -> Dict[str, Any]:
        data = {
            'from': message.from_email or self.config.get('from_email'),
            'to': message.to,
            'subject': message.subject,
        }

        if message.html:
            data['html'] = message.body
        else:
            data['text'] = message.body

        if message.cc:
            data['cc'] = message.cc
        if message.bcc:
            data['bcc'] = message.bcc

        if message.reply_to:
            data['h:Reply-To'] = message.reply_to

        if message.headers:
            for key, value in message.headers.items():
                data[f'h:{key}'] = value

        return data