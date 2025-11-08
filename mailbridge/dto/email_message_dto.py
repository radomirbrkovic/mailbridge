from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Union, Any


@dataclass
class EmailMessageDto:
    to: Union[str, List[str]]
    subject: Optional[str] = None
    body: Optional[str] = None
    from_email: Optional[str] = None
    cc: Optional[Union[str, List[str]]] = None
    bcc: Optional[Union[str, List[str]]] = None
    reply_to: Optional[str] = None
    attachments: Optional[List[Union[Path, tuple]]] = None
    html: bool = True
    headers: Optional[Dict[str, str]] = None
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


    def __post_init__(self):
        """Normalize email addresses to lists."""
        if isinstance(self.to, str):
            self.to = [self.to]
        if isinstance(self.cc, str):
            self.cc = [self.cc]
        if isinstance(self.bcc, str):
            self.bcc = [self.bcc]

        if not self.template_id and not self.subject:
            raise ValueError("Either 'subject' or 'template_id' must be provided")

        if not self.template_id and not self.body:
            raise ValueError("Either 'body' or 'template_id' must be provided")

    def is_template_email(self) -> bool:
        """Check if this is a template-based email."""
        return self.template_id is not None