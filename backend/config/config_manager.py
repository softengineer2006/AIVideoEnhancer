from pathlib import Path
from typing import Any

import yaml


class ConfigManager:
    """
    Loads and provides access to YAML configuration.
    """

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self._config: dict[str, Any] = {}

    def load(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as file:
            self._config = yaml.safe_load(file) or {}

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Supports nested keys.

        Example:
            get("encoding.codec")
        """

        value = self._config

        for part in key.split("."):
            if not isinstance(value, dict):
                return default

            value = value.get(part)

            if value is None:
                return default

        return value

    def reload(self) -> None:
        self.load()