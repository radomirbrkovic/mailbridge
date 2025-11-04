import base64
from pathlib import Path
from typing import Dict, Any, List
import requests
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.exceptions import ConfigurationError, EmailSendError

class SendGridProvider(BaseEmailProvider):
    def _validate_config(self) -> None:
        """Validate SendGrid configuration."""
        if 'api_key' not in self.config:
            raise ConfigurationError("Missing required SendGrid configuration: api_key")

        self.endpoint = self.config.get(
            'endpoint',
            'https://api.sendgrid.com/v3/mail/send'
        )

    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        """Send email via SendGrid API."""
        try:
            payload = self._build_payload(message)

            headers = {
                'Authorization': f'Bearer {self.config["api_key"]}',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code not in (200, 202):
                raise EmailSendError(
                    f"SendGrid API error: {response.status_code} - {response.text}",
                    provider='sendgrid'
                )

            return {
                'success': True,
                'message_id': response.headers.get('X-Message-Id'),
                'status_code': response.status_code,
                'provider': 'sendgrid'
            }

        except requests.RequestException as e:
            raise EmailSendError(
                f"Failed to send email via SendGrid: {str(e)}",
                provider='sendgrid',
                original_error=e
            )

    def _build_payload(self, message: EmailMessageDto) -> Dict[str, Any]:
        """Build SendGrid API payload."""
        payload = {
            'personalizations': [{
                'to': [{'email': email} for email in message.to]
            }],
            'from': {
                'email': message.from_email or self.config.get('from_email')
            },
            'subject': message.subject,
            'content': [{
                'type': 'text/html' if message.html else 'text/plain',
                'value': message.body
            }]
        }

        # Add CC
        if message.cc:
            payload['personalizations'][0]['cc'] = [
                {'email': email} for email in message.cc
            ]

        # Add BCC
        if message.bcc:
            payload['personalizations'][0]['bcc'] = [
                {'email': email} for email in message.bcc
            ]

        # Add Reply-To
        if message.reply_to:
            payload['reply_to'] = {'email': message.reply_to}

        # Add custom headers
        if message.headers:
            payload['headers'] = message.headers

        # Add attachments
        if message.attachments:
            payload['attachments'] = self._build_attachments(message.attachments)

        return payload

    def _build_attachments(self, attachments: List) -> List[Dict[str, str]]:
        """Build attachments payload."""
        result = []

        for attachment in attachments:
            if isinstance(attachment, Path):
                with open(attachment, 'rb') as f:
                    content = base64.b64encode(f.read()).decode()
                result.append({
                    'content': content,
                    'filename': attachment.name,
                    'type': 'application/octet-stream',
                    'disposition': 'attachment'
                })
            elif isinstance(attachment, tuple):
                filename, content, mimetype = attachment
                if isinstance(content, str):
                    content = content.encode()
                encoded = base64.b64encode(content).decode()
                result.append({
                    'content': encoded,
                    'filename': filename,
                    'type': mimetype,
                    'disposition': 'attachment'
                })

        return result
