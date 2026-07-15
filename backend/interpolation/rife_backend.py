import importlib
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn.functional as F

from backend.interpolation.models import InterpolationResult
from backend.interpolation.rife_options import RIFEOptions


class RIFEBackend:

    VALID_FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    def __init__(
        self,
        repository_path: Path,
        model_directory: Path,

    ):

        self.repository_path = repository_path

        self.model_directory = model_directory

        self.verify()

        self.model = None
        self.torch_device = None
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

    @staticmethod
    def _resolve_device(requested: str) -> torch.device:

        if requested == "auto":
            return torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )

        return torch.device(requested)

    def _load_model(self, requested_device: str = "auto"):

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

        self.torch_device = self._resolve_device(requested_device)

        self.loaded = True

    @staticmethod
    def _list_frames(directory: Path) -> list[Path]:

        return [
            file
            for file in sorted(Path(directory).iterdir())
            if file.is_file()
            and file.suffix.lower() in RIFEBackend.VALID_FORMATS
        ]

    def _read_tensor(self, path: Path):

        image = cv2.imread(str(path), cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError(f"Unable to read frame: {path}")

        image = image[:, :, ::-1].copy()  # BGR -> RGB

        tensor = torch.from_numpy(
            np.transpose(image, (2, 0, 1))
        ).to(self.torch_device).unsqueeze(0).float() / 255.0

        return tensor, image.shape[0], image.shape[1]

    @staticmethod
    def _pad(tensor, height, width, multiple=64):

        pad_h = ((height - 1) // multiple + 1) * multiple - height
        pad_w = ((width - 1) // multiple + 1) * multiple - width

        return F.pad(tensor, (0, pad_w, 0, pad_h))

    @staticmethod
    def _write_tensor(tensor, height, width, path: Path):

        array = (
            (tensor[0] * 255.0)
            .clamp(0, 255)
            .byte()
            .cpu()
            .numpy()
            .transpose(1, 2, 0)[:height, :width]
        )

        array = array[:, :, ::-1]  # RGB -> BGR

        cv2.imwrite(str(path), array)

    def _infer_middle(self, img0_padded, img1_padded, timestep: float):
        try:
            return self.model.inference(
                img0_padded,
                img1_padded,
                timestep=timestep,
            )
        except TypeError:
            # Older RIFE builds don't accept a `timestep` kwarg and
            # only support the fixed midpoint (t=0.5).
            return self.model.inference(
                img0_padded,
                img1_padded,
            )

    def interpolate_directory(
        self,
        input_directory: Path,
        output_directory: Path,
        options: RIFEOptions,
    ):

        # Guard against callers accidentally passing the class itself
        # instead of an instance (e.g. `options=RIFEOptions`).
        if isinstance(options, type):
            options = options()

        self._load_model(options.device)

        print("RIFE Model Loaded Successfully")

        input_directory = Path(input_directory)
        output_directory = Path(output_directory)

        output_directory.mkdir(parents=True, exist_ok=True)

        for file in output_directory.iterdir():
            if file.is_file():
                file.unlink()

        frames = self._list_frames(input_directory)

        if len(frames) < 2:
            raise ValueError(
                "At least 2 input frames are required for interpolation."
            )

        multi = max(int(options.multi), 1)

        total_planned = (len(frames) - 1) * multi + 1
        digits = len(str(total_planned))

        output_index = 0

        def save_frame(tensor, height, width):
            nonlocal output_index
            name = f"frame_{output_index:0{digits}d}.png"
            self._write_tensor(tensor, height, width, output_directory / name)
            output_index += 1

        with torch.no_grad():

            current_tensor, height, width = self._read_tensor(frames[0])
            current_padded = self._pad(current_tensor, height, width)

            save_frame(current_tensor, height, width)

            for next_frame in frames[1:]:

                next_tensor, n_height, n_width = self._read_tensor(next_frame)

                if (n_height, n_width) != (height, width):
                    raise ValueError(
                        f"Frame size mismatch at {next_frame}: "
                        f"expected {(height, width)}, got {(n_height, n_width)}"
                    )

                next_padded = self._pad(next_tensor, height, width)

                for step in range(1, multi):

                    timestep = step / multi

                    middle = self._infer_middle(
                        current_padded,
                        next_padded,
                        timestep,
                    )

                    save_frame(middle, height, width)

                    if options.verbose:
                        print(
                            f"Generated intermediate frame {output_index} "
                            f"(t={timestep:.3f})"
                        )

                save_frame(next_tensor, height, width)

                current_padded = next_padded

        print(
            f"RIFE interpolation complete: {len(frames)} input frames -> "
            f"{output_index} output frames "
            f"(multi={multi}, target_fps={options.target_fps})"
        )

        return InterpolationResult(
            input_directory=str(input_directory),
            output_directory=str(output_directory),
            target_fps=options.target_fps,
            success=True,
        )