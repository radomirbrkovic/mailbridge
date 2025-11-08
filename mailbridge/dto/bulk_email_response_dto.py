from dataclasses import dataclass, field
from typing import List
from mailbridge.dto.email_response_dto import EmailResponseDTO


@dataclass
class BulkEmailResponseDTO:
    total: int
    successful: int
    failed: int
    responses: List[EmailResponseDTO] = field(default_factory=list)

    @classmethod
    def from_responses(cls, responses: List[EmailResponseDTO]) -> 'BulkEmailResponseDTO':
        total = len(responses)
        successful = sum(1 for r in responses if r.success)
        failed = total - successful

        return cls(
            total=total,
            successful=successful,
            failed=failed,
            responses=responses
        )