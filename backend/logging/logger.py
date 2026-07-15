from pathlib import Path
import logging
import logging.config

import yaml


class LoggerManager:
    """
    Configures application logging.
    """

    def __init__(self, config_file: Path):

        self.config_file = config_file

    def setup(self) -> None:

        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Logging configuration not found: {self.config_file}"
            )

        with open(self.config_file, "r", encoding="utf-8") as file:

            config = yaml.safe_load(file)

        Path("logs").mkdir(exist_ok=True)

        logging.config.dictConfig(config)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:

        return logging.getLogger(name)