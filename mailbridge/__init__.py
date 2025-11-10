"""
MailBridge - Unified email library with multi-provider support.

Usage:
    from mailbridge import MailBridge

    mailer = MailBridge(provider='sendgrid', api_key='xxx')
    mailer.send(to='user@example.com', subject='Hi', body='Hello!')
"""

# Main client
from mailbridge.client import MailBridge

# DTOs (optional - for users who need them)
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.email_response_dto import EmailResponseDTO
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.dto.bulk_email_response_dto import BulkEmailResponseDTO

# Exceptions (optional - for error handling)
from mailbridge.exceptions import (
    MailBridgeError,
    ConfigurationError,
    EmailSendError,
    ProviderNotFoundError
)

# Version
__version__ = '2.0.0'

# Public API
__all__ = [
    # Main class
    'MailBridge',

    # DTOs
    'EmailMessageDto',
    'EmailResponseDTO',
    'BulkEmailDTO',
    'BulkEmailResponseDTO',

    # Exceptions
    'MailBridgeError',
    'ConfigurationError',
    'EmailSendError',
    'ProviderNotFoundError',
]