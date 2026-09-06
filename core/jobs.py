from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from core.exceptions import JobNotFoundError
from core.results import ExecutionResult


class JobStatus(str, Enum):

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """
    Represents one tool execution.
    """

    tool_name: str
    command: list[str]

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    status: JobStatus = JobStatus.QUEUED

    created_at: datetime = field(
        default_factory=datetime.now
    )

    started_at: datetime | None = None
    finished_at: datetime | None = None

    result: ExecutionResult | None = None
    error: str | None = None


class JobManager:
    """
    In-memory job manager.
    """

    def __init__(self) -> None:

        self._jobs: dict[str, Job] = {}

    def create(
        self,
        tool_name: str,
        command: list[str],
    ) -> Job:

        job = Job(
            tool_name=tool_name,
            command=command,
        )

        self._jobs[job.id] = job

        return job

    def get(
        self,
        job_id: str,
    ) -> Job:

        job = self._jobs.get(job_id)

        if job is None:
            raise JobNotFoundError(
                f"Job '{job_id}' was not found."
            )

        return job

    def all(self) -> list[Job]:

        return list(
            self._jobs.values()
        )

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
    ) -> Job:

        job = self.get(job_id)

        job.status = status

        if status == JobStatus.RUNNING:

            job.started_at = datetime.now()

        elif status in {
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        }:

            job.finished_at = datetime.now()

        return job

    def attach_result(
        self,
        job_id: str,
        result: ExecutionResult,
    ) -> Job:

        job = self.get(job_id)

        job.result = result

        if result.success:

            self.update_status(
                job_id,
                JobStatus.COMPLETED,
            )

        else:

            job.error = result.stderr

            self.update_status(
                job_id,
                JobStatus.FAILED,
            )

        return job