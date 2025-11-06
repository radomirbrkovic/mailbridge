from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class EmailResponseDTO:
    success: bool
    message_id: Optional[str] = None
    provider: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)