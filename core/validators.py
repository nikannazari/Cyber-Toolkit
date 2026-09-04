import shutil
from ipaddress import ip_address
from urllib.parse import urlparse

from core.exceptions import ToolValidationError


def require_binary(binary: str) -> str:
    """
    Verify that a binary exists in PATH.
    """

    path = shutil.which(binary)

    if path is None:
        raise ToolValidationError(
            f"Required binary '{binary}' was not found."
        )

    return path


def require_non_empty(value: str, field_name: str) -> str:
    """
    Validate that a string is not empty.
    """

    value = value.strip()

    if not value:
        raise ToolValidationError(
            f"{field_name} cannot be empty."
        )

    return value


def validate_ip(value: str) -> str:
    """
    Validate an IPv4 or IPv6 address.
    """

    try:
        ip_address(value)
    except ValueError as exc:
        raise ToolValidationError(
            f"Invalid IP address: {value}"
        ) from exc

    return value


def validate_url(value: str) -> str:
    """
    Validate a basic HTTP/HTTPS URL.
    """

    parsed = urlparse(value)

    if parsed.scheme not in {"http", "https"}:
        raise ToolValidationError(
            "URL must use HTTP or HTTPS."
        )

    if not parsed.netloc:
        raise ToolValidationError(
            f"Invalid URL: {value}"
        )

    return value