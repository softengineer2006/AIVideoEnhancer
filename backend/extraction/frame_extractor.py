from pathlib import Path

from backend.core.ffmpeg_manager import FFmpegManager


class FrameExtractor:
    """
    Extracts frames from a video using FFmpeg.
    """

    def __init__(self) -> None:
        self.ffmpeg = FFmpegManager()

    def extract(
        self,
        input_video: Path,
        output_directory: Path,
        fps: float | None = 5.0,
        image_format: str = "jpg",
    ) -> int:

        self.ffmpeg.verify_video(input_video)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        image_format = image_format.lower()

        if image_format not in ("png", "jpg", 'webp'):
            raise ValueError(
                "image_format must be 'png' or 'jpg' or 'webp'"
            )

        for image in output_directory.glob("*"):
            if image.is_file():
                image.unlink()

        output_pattern = (
            output_directory / f"frame_%06d.{image_format}"
        )

        command = [
            "-y",
            "-i",
            str(input_video),
        ]

        if fps is not None:
            command.extend([
                "-vf",
                f"fps={fps}",
            ])

        command.append(str(output_pattern))

        self.ffmpeg.execute_ffmpeg(command)

        return len(list(output_directory.glob(f"*.{image_format}")))