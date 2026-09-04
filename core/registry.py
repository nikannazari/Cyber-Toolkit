from core.exceptions import ToolNotFoundError
from core.tool import Tool


class ToolRegistry:
    """
    Central registry for CyberToolkit tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool.
        """
        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """
        Retrieve a tool by name.
        """
        try:
            return self._tools[name]
        except KeyError:
            raise ToolNotFoundError(
                f"Tool '{name}' is not registered."
            )

    def all(self) -> list[Tool]:
        """
        Return all registered tools.
        """
        return list(self._tools.values())

    def names(self) -> list[str]:
        """
        Return registered tool names.
        """
        return list(self._tools.keys())

    def categories(self) -> dict[str, list[Tool]]:
        """
        Group tools by category.
        """
        result: dict[str, list[Tool]] = {}

        for tool in self._tools.values():
            result.setdefault(tool.category, []).append(tool)

        return result