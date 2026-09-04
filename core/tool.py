from abc import ABC, abstractmethod
from typing import Any


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
        """Check whether the underlying executable is available."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, options: dict[str, Any]) -> None:
        """Validate tool options."""
        raise NotImplementedError

    @abstractmethod
    def build_command(self, options: dict[str, Any]) -> list[str]:
        """Build a safe command argument list."""
        raise NotImplementedError

    def info(self) -> dict[str, Any]:
        """
        Return metadata about the tool.
        """
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "binary": self.binary,
            "version": self.version,
            "available": self.is_available(),
        }