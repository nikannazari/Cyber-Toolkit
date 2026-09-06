from core.exceptions import (
    ToolAlreadyRegisteredError,
    ToolNotFoundError,
)
from core.tool import Tool


class ToolRegistry:
    """
    Central registry for CyberToolkit tools.
    """

    def __init__(self) -> None:

        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:

        if tool.name in self._tools:

            raise ToolAlreadyRegisteredError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:

        if name not in self._tools:

            raise ToolNotFoundError(
                f"Tool '{name}' is not registered."
            )

        del self._tools[name]

    def get(
        self,
        name: str,
    ) -> Tool:

        tool = self._tools.get(name)

        if tool is None:

            raise ToolNotFoundError(
                f"Tool '{name}' is not registered."
            )

        return tool

    def all(self) -> list[Tool]:

        return list(
            self._tools.values()
        )

    def names(self) -> list[str]:

        return list(
            self._tools.keys()
        )

    def categories(
        self,
    ) -> dict[str, list[Tool]]:

        categories: dict[str, list[Tool]] = {}

        for tool in self._tools.values():

            categories.setdefault(
                tool.category,
                [],
            ).append(tool)

        return categories

    def count(self) -> int:

        return len(self._tools)