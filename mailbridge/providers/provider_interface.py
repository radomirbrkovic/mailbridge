from abc import ABC, abstractmethod

class ProviderInterface(ABC):
    @abstractmethod
    def send(self, to:str, subject: str, body: str, from_email: str = None):
        """Send an email through this provider."""
        pass