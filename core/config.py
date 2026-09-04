from pathlib import Path

import yaml


class Config:
    """
    Application configuration loader.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data: dict = {}

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
            self.data = yaml.safe_load(file) or {}

    def get(
        self,
        key: str,
        default=None,
    ):
        """
        Get a top-level configuration value.
        """

        return self.data.get(key, default)