from pathlib import Path

from backend.interpolation.rife_backend import RIFEBackend
from backend.interpolation.rife_options import RIFEOptions


class InterpolationEngine:

    def __init__(self):

        self.backend = None

    def use_rife(
        self,
        repository_path: Path,
        model_directory: Path,
    ):

        self.backend = RIFEBackend(
            repository_path,
            model_directory,
        )

    def interpolate_directory(
        self,
        input_directory: Path,
        output_directory: Path,
        options: RIFEOptions,
    ):

        if self.backend is None:
            raise RuntimeError(
                "Interpolation backend not configured."
            )

        return self.backend.interpolate_directory(
            input_directory,
            output_directory,
            options,
        )