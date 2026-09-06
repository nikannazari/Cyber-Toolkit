from typing import Any

from core.exceptions import ToolValidationError
from core.option import ToolOption
from core.tool import Tool
from core.validators import (
    require_binary,
    require_non_empty,
)


class ExampleTool(Tool):
    """
    Simple tool used to verify CyberToolkit.
    """

    name = "example"

    description = (
        "Simple test tool used for framework development."
    )

    category = "examples"

    binary = "echo"

    version = "1.0"

    def is_available(self) -> bool:

        try:

            require_binary(
                self.binary
            )

            return True

        except ToolValidationError:

            return False

    def options(self) -> list[ToolOption]:
        """
        Describe the options displayed by the UI.
        """

        return [
            ToolOption(
                name="message",
                label="Message",
                type="text",
                required=True,
                default="Hello from CyberToolkit!",
                description=(
                    "Message that will be passed to echo."
                ),
                placeholder="Enter a message...",
            )
        ]

    def validate(
        self,
        options: dict[str, Any],
    ) -> None:

        message = options.get(
            "message"
        )

        require_non_empty(
            message,
            "message",
        )

    def build_command(
        self,
        options: dict[str, Any],
    ) -> list[str]:

        self.validate(
            options
        )

        message = options[
            "message"
        ].strip()

        return [
            self.binary,
            message,
        ]