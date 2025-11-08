from dataclasses import dataclass
from typing import List, Optional

from mailbridge.dto.email_message_dto import EmailMessageDto


@dataclass
class BulkEmailDTO:

    messages: List[EmailMessageDto]
    default_from: Optional[str] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        if not self.messages:
            raise ValueError("At least one message must be provided")

        if self.default_from:
            for message in self.messages:
                if not message.from_email:
                    message.from_email = self.default_from

        if self.tags:
            for message in self.messages:
                if message.tags:
                    message.tags.extend(self.tags)
                else:
                    message.tags = self.tags.copy()
