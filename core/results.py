from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ExecutionResult:
    """
    Represents the result of a tool execution.
    """

    command: list[str]
    stdout: str
    stderr: str
    return_code: int
    started_at: datetime
    finished_at: datetime

    @property
    def success(self) -> bool:
        """Return True when the process completed successfully."""
        return self.return_code == 0

    @property
    def duration(self) -> float:
        """Return execution duration in seconds."""
        return (
            self.finished_at - self.started_at
        ).total_seconds()