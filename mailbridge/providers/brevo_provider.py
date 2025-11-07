import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from mailbridge.providers.base_email_provider import BaseEmailProvider, BulkCapableProvider
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.dto.bulk_email_response_dto import BulkEmailResponseDTO
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.email_response_dto import EmailResponseDTO
from mailbridge.exceptions import ConfigurationError, EmailSendError

class BrevoProvider(BaseEmailProvider):
    def send(self, message: EmailMessageDto) -> EmailResponseDTO:
        try:
            payload = self._build_payload(message)

            headers = {
                'api-key': self.config['api_key'],
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code not in (200, 201):
                error_data = response.json()
                raise EmailSendError(
                    f"Brevo API error: {error_data.get('code')} - "
                    f"{error_data.get('message')}",
                    provider='brevo'
                )

            result = response.json()

            return EmailResponseDTO(
                success=True,
                message_id=result.get('messageId'),
                provider='brevo',
                metadata={
                    'status_code': response.status_code
                }
            )

        except requests.RequestException as e:
            raise EmailSendError(
                f"Failed to send email via Brevo: {str(e)}",
                provider='brevo',
                original_error=e
            )

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

        if message.is_template_email():
            payload['templateId'] = message.template_id
            payload['params'] = message.template_data or {}
        else:
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

    def _build_attachments(self, attachments: List) -> List[Dict[str, str]]:
        result = []

        for attachment in attachments:
            if isinstance(attachment, Path):
                with open(attachment, 'rb') as f:
                    content = base64.b64encode(f.read()).decode()
                result.append({
                    'name': attachment.name,
                    'content': content
                })
            elif isinstance(attachment, tuple):
                filename, content, mimetype = attachment
                if isinstance(content, str):
                    content = content.encode()
                encoded = base64.b64encode(content).decode()
                result.append({
                    'name': filename,
                    'content': encoded
                })

        return result