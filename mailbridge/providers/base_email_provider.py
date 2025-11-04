from abc import ABC, abstractmethod
from typing import Dict, Any

from mailbridge.dto.email_message_dto import EmailMessageDto

class BaseEmailProvider(ABC):
    def __init__(self, **config):
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """Validate required configuration parameters."""
        pass

    @abstractmethod
    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        """Send an email through this provider."""
        pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup connections."""
        self.close()

    def close(self) -> None:
        """Close any open connections. Override if needed."""
        pass