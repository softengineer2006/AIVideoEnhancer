from pathlib import Path

from backend.enhancement.model_loader import ModelLoader
from backend.enhancement.model_registry import ModelRegistry


class ModelManager:

    def __init__(
        self,
        project_root: Path,
    ):

        self.project_root = project_root

        self.registry = ModelRegistry(
            project_root
            / "config"
            / "models.yaml"
        )

    def get_model(
        self,
        category: str,
        model_name: str,
    ) -> Path:

        info = self.registry.get(
            category,
            model_name,
        )

        if category == "super_resolution":

            directory = (
                self.project_root
                / "models"
                / "realesrgan"
            )

        elif category == "frame_interpolation":

            directory = (
                self.project_root
                / "models"
                / "rife"
            )

        else:

            raise ValueError(category)

        model = directory / info["file"]

        loader = ModelLoader(model)

        loader.verify()

        return model
