from pathlib import Path
from backend.core.ffmpeg_manager import FFmpegManager


class VideoEncoder:
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
        pattern: str = "frame_*.png",
    ) -> Path:
        input_directory = Path(input_directory)
        output_video = Path(output_video)

        frames = sorted(input_directory.glob(pattern))
        if not frames:
            raise FileNotFoundError(
                f"No frames matching '{pattern}' found in {input_directory}"
            )

        output_video.parent.mkdir(parents=True, exist_ok=True)

        command = [
            "-y", "-framerate", str(fps),
            "-pattern_type", "glob",
            "-i", str(input_directory / pattern),
            "-c:v", codec,
            "-pix_fmt", pixel_format,
            "-crf", str(crf),
            str(output_video),
        ]
        self.ffmpeg.execute_ffmpeg(command)
        return output_video