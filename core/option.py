from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolOption:
    """
    Describes one configurable option exposed by a tool.
    """

    name: str

    label: str

    type: str = "text"

    required: bool = False

    default: Any = None

    description: str | None = None

    choices: list[Any] = field(
        default_factory=list
    )

    min_value: int | float | None = None

    max_value: int | float | None = None

    step: int | float | None = None

    placeholder: str | None = None

    section: str = "Basic"

    advanced: bool = False

    visible: bool = True