from abc import ABC, abstractmethod
from typing import Any

from core.option import ToolOption


class Tool(ABC):
    """
    Base interface for every CyberToolkit tool.
    """

    name: str
    description: str
    category: str
    binary: str
    version: str = "unknown"

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check whether the underlying executable is available.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(
        self,
        options: dict[str, Any],
    ) -> None:
        """
        Validate user-provided options.
        """
        raise NotImplementedError

    @abstractmethod
    def build_command(
        self,
        options: dict[str, Any],
    ) -> list[str]:
        """
        Convert structured options into command arguments.
        """
        raise NotImplementedError

    def options(self) -> list[ToolOption]:
        """
        Return the options required by this tool.

        Tools can override this method to expose
        their configuration to the UI.
        """

        return []

    def info(self) -> dict[str, Any]:
        """
        Return public metadata about the tool.
        """

        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "binary": self.binary,
            "version": self.version,
            "available": self.is_available(),
        }