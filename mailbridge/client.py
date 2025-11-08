from typing import Optional, Dict, Any, Union, List
from pathlib import Path

from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.email_response_dto import EmailResponseDTO
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.dto.bulk_email_response_dto import BulkEmailResponseDTO
from mailbridge.exceptions import ProviderNotFoundError
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.providers.brevo_provider import BrevoProvider
from mailbridge.providers.mailgun_provider import MailgunProvider
from mailbridge.providers.postmark_provider import PostmarkProvider
from mailbridge.providers.sendgrid_provider import SendGridProvider
from mailbridge.providers.ses_provider import SESProvider
from mailbridge.providers.smtp_provider import SMTPProvider

class MailBridge:

    PROVIDERS = {
        'smtp': SMTPProvider,
        'sendgrid': SendGridProvider,
        'mailgun': MailgunProvider,
        'ses': SESProvider,
        'postmark': PostmarkProvider,
        'brevo': BrevoProvider,
    }

    def __init__(self, provider: str, **config):
        self.provider_name = provider.lower()
        if self.provider_name not in self.PROVIDERS:
            available = ', '.join(self.PROVIDERS.keys())
            raise ProviderNotFoundError(
                f"Provider '{provider}' not found. Available providers: {available}"
            )

        provider_class = self.PROVIDERS[self.provider_name]
        self.provider: BaseEmailProvider = provider_class(**config)

    def send(
            self,
            to: Union[str, List[str]],
            subject: str,
            body: str,
            from_email: Optional[str] = None,
            cc: Optional[Union[str, List[str]]] = None,
            bcc: Optional[Union[str, List[str]]] = None,
            reply_to: Optional[str] = None,
            attachments: Optional[List[Union[Path, tuple]]] = None,
            html: bool = True,
            headers: Optional[Dict[str, str]] = None,
            template_id: Optional[str] = None,
            template_data: Optional[Dict[str, Any]] = None,
            tags: Optional[List[str]] = None
    ) -> EmailResponseDTO:
        """
        Send an email.

        Args:
            to: Recipient email address(es)
            subject: Email subject
            body: Email body (HTML or plain text)
            from_email: Sender email address (optional if set in config)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            reply_to: Reply-To address (optional)
            attachments: List of file paths or tuples (filename, content, mimetype)
            html: Whether body is HTML (default: True)
            headers: Custom headers (optional)
            template_id: Template id (optional)
            template_data: Template varibales (optional)
            tags: Tags (optional)

        Returns:
            Dict with response data (success, message_id, etc.)

        Raises:
            EmailSendError: If sending fails

        Examples:
            >>> mailer.send(
            ...     to='user@example.com',
            ...     subject='Welcome',
            ...     body='<h1>Hello!</h1>'
            ... )

            >>> mailer.send(
            ...     to=['user1@example.com', 'user2@example.com'],
            ...     subject='Newsletter',
            ...     body='Content here',
            ...     attachments=[Path('report.pdf')]
            ... )
        """
        message = EmailMessageDto(
            to=to,
            subject=subject,
            body=body,
            from_email=from_email,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            attachments=attachments,
            html=html,
            headers=headers,
            template_id=template_id,
            template_data=template_data,
            tags=tags
        )

        return self.provider.send(message)

    def send_bulk(
            self,
            messages: Union[List[EmailMessageDto], BulkEmailDTO],
            default_from: str = None,
            tags: List[str] = None
    ) -> BulkEmailResponseDTO:
        """
        Send multiple emails at once.

        Args:
            messages: List of EmailMessageDto or BulkEmailDTO
            default_from: Default sender email (optional)
            tags: Common tags for all messages (optional)

        Returns:
            BulkEmailResponseDTO with results

        Example:
            messages = [
                EmailMessageDto(to='user1@example.com', subject='Hi', body='Hello 1'),
                EmailMessageDto(to='user2@example.com', subject='Hi', body='Hello 2'),
            ]

            result = mailer.send_bulk(messages)
            print(f"Sent: {result.successful}/{result.total}")
        """
        # If already a BulkEmailDTO, use it directly
        if isinstance(messages, BulkEmailDTO):
            return self.provider.send_bulk(messages)

        # Otherwise, create BulkEmailDTO from list
        bulk = BulkEmailDTO(
            messages=messages,
            default_from=default_from,
            tags=tags
        )

        return self.provider.send_bulk(bulk)

    def supports_templates(self) -> bool:
        """
        Check if current provider supports template emails.

        Returns:
            True if templates are supported, False otherwise
        """
        return self.provider.supports_templates()

    def supports_bulk_sending(self) -> bool:
        """
        Check if current provider has native bulk sending API.

        Returns:
            True if native bulk API exists, False otherwise
        """
        return self.provider.supports_bulk_sending()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.provider.close()

    def close(self):
        """Close provider connection."""
        self.provider.close()

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """
        Register a custom provider.

        Args:
            name: Provider name
            provider_class: Provider class (must inherit from BaseEmailProvider)

        Example:
            >>> class MyProvider(BaseEmailProvider):
            ...     def send(self, message):
            ...         # Implementation
            ...         pass
            >>> MailBridge.register_provider('myprovider', MyProvider)
        """
        if not issubclass(provider_class, BaseEmailProvider):
            raise TypeError(f"{provider_class} must inherit from EmailProvider")
        cls.PROVIDERS[name.lower()] = provider_class

    @classmethod
    def available_providers(cls) -> List[str]:
        """
        Get list of available providers.

        Returns:
            List of provider names
        """
        return list(cls.PROVIDERS.keys())