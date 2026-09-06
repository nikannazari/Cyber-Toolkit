from pathlib import Path
from typing import Any

import yaml


class Config:
    """
    Simple YAML configuration loader.
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self.path = Path(path)
        self.data: dict[str, Any] = {}

    def load(self) -> None:
        """
        Load configuration from YAML.
        """

        if not self.path.exists():
            self.data = {}
            return

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:

            loaded = yaml.safe_load(file)

        self.data = (
            loaded
            if isinstance(loaded, dict)
            else {}
        )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.data.get(
            key,
            default,
        )

    def get_section(
        self,
        section: str,
    ) -> dict[str, Any]:

        value = self.data.get(
            section,
            {},
        )

        return (
            value
            if isinstance(value, dict)
            else {}
        )