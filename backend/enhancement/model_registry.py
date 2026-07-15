from pathlib import Path

import yaml


class ModelRegistry:

    def __init__(self, registry_file: Path):

        self.registry_file = registry_file

        self.models = {}

        self.load()

    def load(self):

        with open(
            self.registry_file,
            "r",
            encoding="utf-8",
        ) as f:

            self.models = yaml.safe_load(f)

    def get(self, category: str, name: str):

        if category not in self.models:
            raise KeyError(category)

        if name not in self.models[category]:
            raise KeyError(name)

        return self.models[category][name]