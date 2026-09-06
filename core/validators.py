import re
import shutil

from ipaddress import ip_address
from urllib.parse import urlparse

from core.exceptions import ToolValidationError


def require_binary(binary: str) -> str:
    """
    Return the executable path if it exists.
    """

    path = shutil.which(binary)

    if path is None:
        raise ToolValidationError(
            f"Required binary '{binary}' was not found in PATH."
        )

    return path


def require_non_empty(
    value: str,
    field_name: str,
) -> str:
    """
    Require a non-empty string.
    """

    if not isinstance(value, str):
        raise ToolValidationError(
            f"{field_name} must be a string."
        )

    value = value.strip()

    if not value:
        raise ToolValidationError(
            f"{field_name} cannot be empty."
        )

    return value


def validate_ip(
    value: str,
) -> str:
    """
    Validate an IPv4 or IPv6 address.
    """

    value = require_non_empty(
        value,
        "IP address",
    )

    try:
        ip_address(value)

    except ValueError as exc:
        raise ToolValidationError(
            f"Invalid IP address: {value}"
        ) from exc

    return value


def validate_url(
    value: str,
) -> str:
    """
    Validate HTTP/HTTPS URL.
    """

    value = require_non_empty(
        value,
        "URL",
    )

    parsed = urlparse(value)

    if parsed.scheme not in {
        "http",
        "https",
    }:
        raise ToolValidationError(
            "URL must use HTTP or HTTPS."
        )

    if not parsed.netloc:
        raise ToolValidationError(
            f"Invalid URL: {value}"
        )

    return value


def validate_ports(
    value: str,
) -> str:
    """
    Validate a basic Nmap port specification.

    Examples:

        80
        22,80,443
        1-1000
        22,80,1000-2000
    """

    value = require_non_empty(
        value,
        "ports",
    )

    pattern = (
        r"^\d+(?:-\d+)?"
        r"(?:,\d+(?:-\d+)?)*$"
    )

    if not re.fullmatch(
        pattern,
        value,
    ):
        raise ToolValidationError(
            "Invalid port specification. "
            "Examples: 80, 22,80,443, or 1-1000."
        )

    parts = value.split(",")

    for part in parts:

        if "-" in part:

            start, end = map(
                int,
                part.split("-"),
            )

            if start < 1 or end > 65535:
                raise ToolValidationError(
                    "Ports must be between 1 and 65535."
                )

            if start > end:
                raise ToolValidationError(
                    f"Invalid port range: {part}"
                )

        else:

            port = int(part)

            if not 1 <= port <= 65535:
                raise ToolValidationError(
                    f"Port must be between 1 and 65535: {port}"
                )

    return value