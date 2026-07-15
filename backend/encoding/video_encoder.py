import re
import subprocess
from pathlib import Path

from backend.core.ffmpeg_manager import FFmpegManager


class VideoEncoder:
    """
    Encodes a directory of image frames into a video file using FFmpeg.
    """

    def __init__(self) -> None:
        self.ffmpeg = FFmpegManager()

    def encode_directory(
        self,
        input_directory: Path,
        output_video: Path,
        fps: float,
        codec: str = "libx264",
        crf: int = 18,
        pixel_format: str = "yuv420p",
        stem: str = "frame",
        extension: str = "png",
    ) -> Path:
        """
        Encodes all `{stem}_<digits>.{extension}` frames inside
        `input_directory` into a single video file at the given frame rate.

        Uses explicit sequential numbering (-start_number / %0Nd) rather
        than `-pattern_type glob`, since glob support is not compiled
        into every FFmpeg build (notably some minimal static Windows
        builds, e.g. the one bundled by imageio-ffmpeg).
        """

        input_directory = Path(input_directory)
        output_video = Path(output_video)

        frames = sorted(
            input_directory.glob(f"{stem}_*.{extension}")
        )

        if not frames:
            raise FileNotFoundError(
                f"No frames matching '{stem}_*.{extension}' found "
                f"in {input_directory}"
            )

        match = re.search(
            rf"{re.escape(stem)}_(\d+)\.{re.escape(extension)}$",
            frames[0].name,
        )

        if not match:
            raise ValueError(
                f"Could not determine frame numbering pattern from: "
                f"{frames[0].name}"
            )

        digits = len(match.group(1))
        start_number = int(match.group(1))

        output_video.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            "-y",
            "-framerate",
            str(fps),
            "-start_number",
            str(start_number),
            "-i",
            str(input_directory / f"{stem}_%0{digits}d.{extension}"),
            "-c:v",
            codec,
            "-pix_fmt",
            pixel_format,
            "-crf",
            str(crf),
            str(output_video),
        ]

        try:
            self.ffmpeg.execute_ffmpeg(command)
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                "FFmpeg failed while encoding frames to video.\n"
                f"Command: {' '.join(command)}\n"
                f"--- stderr ---\n{error.stderr}"
            ) from error

        return output_video