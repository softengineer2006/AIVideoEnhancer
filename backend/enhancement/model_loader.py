from pathlib import Path


class ModelLoader:

    def __init__(self, model_path: Path):

        self.model_path = model_path

    def exists(self) -> bool:

        return self.model_path.exists()

    def verify(self) -> None:

        if not self.exists():
            raise FileNotFoundError(
                f"Model not found:\n{self.model_path}"
            )