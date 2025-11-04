"""Custom exceptions for MailBridge."""


class MailBridgeError(Exception):
    """Base exception for all MailBridge errors."""
    pass


class ConfigurationError(MailBridgeError):
    """Raised when configuration is invalid or missing."""
    pass


class EmailSendError(MailBridgeError):
    """Raised when email sending fails."""

    def __init__(self, message: str, provider: str = None, original_error: Exception = None):
        self.provider = provider
        self.original_error = original_error
        super().__init__(message)


class ProviderNotFoundError(MailBridgeError):
    """Raised when requested provider is not available."""
    pass


class AttachmentError(MailBridgeError):
    """Raised when there's an issue with attachments."""
    pass