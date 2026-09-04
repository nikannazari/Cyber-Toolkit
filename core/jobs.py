from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """
    Represents a CyberToolkit execution job.
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

    result: object | None = None
    error: str | None = None


class JobManager:
    """
    Manages CyberToolkit jobs.
    """

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}

    def create(
        self,
        tool_name: str,
        command: list[str],
    ) -> Job:
        """
        Create and store a new job.
        """

        job = Job(
            tool_name=tool_name,
            command=command,
        )

        self._jobs[job.id] = job

        return job

    def get(self, job_id: str) -> Job | None:
        """
        Retrieve a job by ID.
        """

        return self._jobs.get(job_id)

    def all(self) -> list[Job]:
        """
        Return all jobs.
        """

        return list(self._jobs.values())

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
    ) -> Job:
        """
        Update a job's status.
        """

        job = self.get(job_id)

        if job is None:
            raise KeyError(
                f"Job '{job_id}' not found."
            )

        job.status = status

        if status == JobStatus.RUNNING:
            job.started_at = datetime.now()

        if status in {
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        }:
            job.finished_at = datetime.now()

        return job