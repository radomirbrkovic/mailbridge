from pathlib import Path
from typing import Dict, Any, List
import requests
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.exceptions import ConfigurationError, EmailSendError

class MailgunProvider(BaseEmailProvider):

    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        try:
            data = self._build_from_data(message)
            files = self._build_files(message.attachments) if message.attachments else None

            # Basic auth sa api key
            auth = ('api', self.config['api_key'])

            response = requests.post(
                f"{self.config.get('endpoint')}/messages",
                auth=auth,
                data=data,
                files=files,
                timeout=30
            )

            if response.status_code != 200:
                raise EmailSendError(
                    f"Mailgun API error: {response.status_code} - {response.text}",
                    provider='mailgun'
                )

            result = response.json()

            return {
                'success': True,
                'message_id': result.get('id'),
                'message': result.get('message'),
                'provider': 'mailgun'
            }

        except requests.RequestException as e:
            raise EmailSendError(
                f"Failed to send email via Mailgun: {str(e)}",
                provider='mailgun',
                original_error=e
            )


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

    def _build_files(self, attachments: List) -> List[tuple]:
        files = []

        for attachment in attachments:
            if isinstance(attachment, Path):
                files.append((
                    'attachment',
                    (attachment.name, open(attachment, 'rb'), 'application/octet-stream')
                ))
            elif isinstance(attachment, tuple):
                filename, content, mimetype = attachment
                if isinstance(content, str):
                    content = content.encode()
                files.append((
                    'attachment',
                    (filename, content, mimetype)
                ))

        return files
