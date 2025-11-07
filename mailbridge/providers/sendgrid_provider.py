import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from mailbridge.providers.base_email_provider import TemplateCapableProvider, BulkCapableProvider
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.dto.bulk_email_response_dto import BulkEmailResponseDTO
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.email_response_dto import EmailResponseDTO
from mailbridge.exceptions import ConfigurationError, EmailSendError

class SendGridProvider(TemplateCapableProvider, BulkCapableProvider):
    def _validate_config(self) -> None:
        """Validate SendGrid configuration."""
        if 'api_key' not in self.config:
            raise ConfigurationError("Missing required SendGrid configuration: api_key")

        self.endpoint = self.config.get(
            'endpoint',
            'https://api.sendgrid.com/v3/mail/send'
        )

    def send(self, message: EmailMessageDto) -> EmailResponseDTO:
        """Send email via SendGrid API."""
        try:

              if message.is_template_email():
                  return self.send_template(
                      template_id=message.template_id,
                      to=message.to,
                      template_data=message.template_data or {},
                      from_email=message.from_email,
                      cc=message.cc,
                      bcc=message.bcc,
                      reply_to=message.reply_to,
                      headers=message.headers,
                      attachments=message.attachments
                  )
              payload = self._build_payload(message)
              response = self._send_request(payload)

              return EmailResponseDTO(
                  success=True,
                  message_id=response.headers.get('X-Message-Id'),
                  provider='sendgrid',
                  metadata={
                      'status_code': response.status_code
                  }
              )

        except requests.RequestException as e:
            raise EmailSendError(
                f"Failed to send email via SendGrid: {str(e)}",
                provider='sendgrid',
                original_error=e
            )

    def send_template(
            self,
            template_id: str,
            to: List[str],
            template_data: Dict[str, Any],
            from_email: Optional[str] = None,
            **kwargs
    ) -> EmailResponseDTO:
        try:
            payload = {
                'personalizations': [{
                    'to': [{'email': email} for email in to],
                    'dynamic_template_data': template_data
                }],
                'from': {
                    'email': from_email or self.config.get('from_email')
                },
                'template_id': template_id
            }

            # Add optional fields
            if kwargs.get('cc'):
                payload['personalizations'][0]['cc'] = [
                    {'email': email} for email in kwargs['cc']
                ]
            if kwargs.get('bcc'):
                payload['personalizations'][0]['bcc'] = [
                    {'email': email} for email in kwargs['bcc']
                ]
            if kwargs.get('reply_to'):
                payload['reply_to'] = {'email': kwargs['reply_to']}
            if kwargs.get('headers'):
                payload['headers'] = kwargs['headers']
            if kwargs.get('attachments'):
                payload['attachments'] = self._build_attachments(kwargs['attachments'])


            response = self._send_request(payload)
            return EmailResponseDTO(
                success=True,
                message_id=response.headers.get('X-Message-Id'),
                provider='sendgrid',
                metadata={
                    'template_id': template_id,
                    'status_code': response.status_code
                }
            )

        except requests.RequestException as e:
            raise EmailSendError(
                f"Failed to send template email via SendGrid: {str(e)}",
                provider='sendgrid',
                original_error=e
            )

    def send_bulk(self, bulk: BulkEmailDTO) -> BulkEmailResponseDTO:
        try:
            # Group messages by template vs regular
            template_messages = [m for m in bulk.messages if m.is_template_email()]
            regular_messages = [m for m in bulk.messages if not m.is_template_email()]

            responses = []

            # Send template messages (can batch by template_id)
            if template_messages:
                grouped_by_template = {}
                for msg in template_messages:
                    if msg.template_id not in grouped_by_template:
                        grouped_by_template[msg.template_id] = []
                    grouped_by_template[msg.template_id].append(msg)

                for template_id, messages in grouped_by_template.items():
                    response = self._send_bulk_template(template_id, messages)
                    responses.append(response)

            # Send regular messages
            for msg in regular_messages:
                response = self.send(msg)
                responses.append(response)

            return BulkEmailResponseDTO.from_responses(responses)

        except Exception as e:
            raise EmailSendError(
                f"Failed to send bulk emails via SendGrid: {str(e)}",
                provider='sendgrid',
                original_error=e
            )

    def _send_bulk_template(
            self,
            template_id: str,
            messages: List[EmailMessageDto]
    ) -> EmailResponseDTO:
        """Send multiple template emails with same template_id."""
        personalizations = []

        for msg in messages:
            personalization = {
                'to': [{'email': email} for email in msg.to],
                'dynamic_template_data': msg.template_data or {}
            }

            if msg.cc:
                personalization['cc'] = [{'email': email} for email in msg.cc]
            if msg.bcc:
                personalization['bcc'] = [{'email': email} for email in msg.bcc]

            personalizations.append(personalization)

        payload = {
            'personalizations': personalizations,
            'from': {
                'email': messages[0].from_email or self.config.get('from_email')
            },
            'template_id': template_id
        }

        response = self._send_request(payload)

        if response.status_code not in (200, 202):
            raise EmailSendError(
                f"SendGrid bulk template error: {response.status_code}",
                provider='sendgrid'
            )

        return EmailResponseDTO(
            success=True,
            message_id=response.headers.get('X-Message-Id'),
            provider='sendgrid',
            metadata={
                'bulk_count': len(messages),
                'template_id': template_id
            }
        )

    def _send_request(self, payload: Dict[str, Any]):
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
                f"SendGrid template error: {response.status_code} - {response.text}",
                provider='sendgrid'
            )

        return requests


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
