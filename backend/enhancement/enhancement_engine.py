from pathlib import Path

from backend.enhancement.ncnn_backend import NCNNBackend
from backend.enhancement.ncnn_options import NCNNOptions


class EnhancementEngine:

    def __init__(self):

        self.backend = None

    def use_ncnn(
        self,
        executable: Path,
        model_directory: Path,
    ) -> None:

        self.backend = NCNNBackend(
            executable,
            model_directory,
        )

    def enhance_directory(
        self,
        input_directory: Path,
        output_directory: Path,
        options: NCNNOptions,
    ):

        if self.backend is None:
            raise RuntimeError(
                "No enhancement backend has been configured."
            )

        return self.backend.enhance_directory(
            input_directory,
            output_directory,
            options,
        )
