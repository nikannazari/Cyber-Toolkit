class CyberToolkitError(Exception):
    """
    Base exception for CyberToolkit.
    """


class ToolError(CyberToolkitError):
    """
    Base exception for tool-related errors.
    """


class ToolNotFoundError(ToolError):
    """
    Raised when a requested tool does not exist.
    """


class ToolAlreadyRegisteredError(ToolError):
    """
    Raised when a tool is registered more than once.
    """


class ToolNotAvailableError(ToolError):
    """
    Raised when a required executable is unavailable.
    """


class ToolValidationError(ToolError):
    """
    Raised when tool input validation fails.
    """


class ExecutionError(CyberToolkitError):
    """
    Raised when command execution fails.
    """


class ExecutionTimeoutError(ExecutionError):
    """
    Raised when command execution exceeds its timeout.
    """


class JobNotFoundError(CyberToolkitError):
    """
    Raised when a requested job does not exist.
    """