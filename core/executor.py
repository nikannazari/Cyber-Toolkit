import os
import subprocess
from datetime import datetime

from core.exceptions import (
    ExecutionError,
    ExecutionTimeoutError,
)

from core.results import ExecutionResult


class Executor:
    """
    Executes external security tools.

    Commands are always passed as argument lists.

    shell=True is never used.
    """

    def __init__(
        self,
        default_timeout: int = 300,
    ) -> None:

        self.default_timeout = default_timeout

    def run(
        self,
        command: list[str],
        timeout: int | None = None,
        environment: dict[str, str] | None = None,
    ) -> ExecutionResult:
        """
        Execute a command and return its result.
        """

        if not command:
            raise ExecutionError(
                "Cannot execute an empty command."
            )

        if not all(
            isinstance(argument, str)
            for argument in command
        ):
            raise ExecutionError(
                "Every command argument must be a string."
            )

        execution_timeout = (
            timeout
            if timeout is not None
            else self.default_timeout
        )

        if execution_timeout <= 0:
            raise ExecutionError(
                "Timeout must be greater than zero."
            )

        env = os.environ.copy()

        if environment is not None:
            env.update(environment)

        started_at = datetime.now()

        try:

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=execution_timeout,
                shell=False,
                env=env,
            )

        except subprocess.TimeoutExpired as exc:

            finished_at = datetime.now()

            raise ExecutionTimeoutError(
                f"Command exceeded timeout of "
                f"{execution_timeout} seconds."
            ) from exc

        except OSError as exc:

            raise ExecutionError(
                f"Failed to execute command: {exc}"
            ) from exc

        finished_at = datetime.now()

        return ExecutionResult(
            command=command,
            stdout=process.stdout,
            stderr=process.stderr,
            return_code=process.returncode,
            started_at=started_at,
            finished_at=finished_at,
        )