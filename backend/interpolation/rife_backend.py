import importlib
import sys
from pathlib import Path

from backend.interpolation.models import InterpolationResult
from backend.interpolation.rife_options import RIFEOptions



class RIFEBackend:

    def __init__(
        self,
        repository_path: Path,
        model_directory: Path,

    ):

        self.repository_path = repository_path

        self.model_directory = model_directory

        self.verify()

        self.model = None
        self.device = None
        self.loaded = False

    def verify(self):

        if not self.repository_path.exists():
            raise FileNotFoundError(
                self.repository_path
            )

        if not self.model_directory.exists():
            raise FileNotFoundError(
                self.model_directory
            )

    def _prepare_imports(self):

        if str(self.repository_path) not in sys.path:
            sys.path.insert(0, str(self.repository_path))

    def _load_model(self):

        if self.loaded:
            return

        self._prepare_imports()

        module = importlib.import_module(
            "train_log.RIFE_HDv3"
        )

        Model = module.Model

        self.model = Model()

        self.model.load_model(
            str(self.model_directory),
            -1,
        )

        self.model.eval()

        self.model.device()

        self.loaded = True

    def interpolate_directory(
        self,
        input_directory: Path,
        output_directory: Path,
        options: RIFEOptions,
    ):
        self._load_model()

        print("RIFE Model Loaded Successfully")
        return InterpolationResult(
            input_directory=str(input_directory),
            output_directory=str(output_directory),
            target_fps=options.target_fps,
            success=True,
        )
