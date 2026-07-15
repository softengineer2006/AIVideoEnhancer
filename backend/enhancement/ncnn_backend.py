from pathlib import Path
import subprocess

from backend.enhancement.models import EnhancementResult
from backend.enhancement.ncnn_options import NCNNOptions


class NCNNBackend:
    """
    Wrapper around the portable Real-ESRGAN NCNN executable.
    """

    def __init__(
        self,
        executable: Path,
        model_directory: Path,
    ) -> None:

        self.executable = executable
        self.model_directory = model_directory

        self.verify()

    def verify(self) -> None:

        if not self.executable.exists():
            raise FileNotFoundError(
                f"Executable not found:\n{self.executable}"
            )

        if not self.model_directory.exists():
            raise FileNotFoundError(
                f"Model directory not found:\n{self.model_directory}"
            )

    def build_command(
        self,
        input_directory: Path,
        output_directory: Path,
        options: NCNNOptions,
    ) -> list[str]:

        command = [
            str(self.executable),

            "-i",
            str(input_directory),

            "-o",
            str(output_directory),

            "-m",
            str(self.model_directory),

            "-n",
            options.model_name,

            "-s",
            str(options.scale),

            "-t",
            str(options.tile_size),

            "-g",
            options.gpu_id,

            "-j",
            options.threads,

            "-f",
            options.output_format,
        ]

        if options.tta:
            command.append("-x")

        if options.verbose:
            command.append("-v")

        return command

    def enhance_directory(
        self,
        input_directory: Path,
        output_directory: Path,
        options: NCNNOptions,
    ) -> EnhancementResult:

        if not input_directory.exists():
            raise FileNotFoundError(
                f"Input directory not found:\n{input_directory}"
            )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = self.build_command(
            input_directory,
            output_directory,
            options,
        )

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if options.verbose:

            print(process.stdout)

            if process.stderr:
                print(process.stderr)

        if process.returncode != 0:
            raise RuntimeError(
                f"Real-ESRGAN failed.\n\n"
                f"Return Code: {process.returncode}\n\n"
                f"STDERR:\n{process.stderr}"
            )

        return EnhancementResult(
            input_directory=str(input_directory),
            output_directory=str(output_directory),
            model=options.model_name,
            scale=options.scale,
            success=True,
        )
