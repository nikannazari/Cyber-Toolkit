from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExecutionResult:
    """
    Result produced by Executor.
    """

    command: list[str]

    stdout: str

    stderr: str

    return_code: int

    started_at: datetime

    finished_at: datetime

    timed_out: bool = False

    @property
    def success(self) -> bool:
        """
        Whether the command completed successfully.
        """

        return (
            self.return_code == 0
            and not self.timed_out
        )

    @property
    def duration(self) -> float:
        """
        Execution duration in seconds.
        """

        return (
            self.finished_at
            - self.started_at
        ).total_seconds()

    @property
    def command_string(self) -> str:
        """
        Human-readable command representation.
        """

        return " ".join(
            self.command
        )

    @property
    def has_output(self) -> bool:
        """
        Whether stdout contains data.
        """

        return bool(
            self.stdout.strip()
        )

    @property
    def has_error(self) -> bool:
        """
        Whether stderr contains data.
        """

        return bool(
            self.stderr.strip()
        )