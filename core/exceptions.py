class CyberToolkitError(Exception):
    """Base exception for CyberToolkit."""


class ToolError(CyberToolkitError):
    """Base exception for tool-related errors."""


class ToolNotFoundError(ToolError):
    """Raised when a requested tool does not exist."""


class ToolNotAvailableError(ToolError):
    """Raised when a tool's executable is not available."""


class ToolValidationError(ToolError):
    """Raised when tool input validation fails."""


class ExecutionError(CyberToolkitError):
    """Raised when a tool execution fails."""


class ExecutionTimeoutError(ExecutionError):
    """Raised when a tool execution exceeds its timeout."""