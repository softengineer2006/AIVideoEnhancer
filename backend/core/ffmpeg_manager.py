from pathlib import Path
import shutil
import subprocess


class FFmpegManager:
    """
    Wrapper for FFmpeg and FFprobe.
    """

    def __init__(self) -> None:

        self.ffmpeg = shutil.which("ffmpeg")
        self.ffprobe = shutil.which("ffprobe")

        if self.ffmpeg is None:
            raise FileNotFoundError("FFmpeg not found in PATH.")

        if self.ffprobe is None:
            raise FileNotFoundError("FFprobe not found in PATH.")

    @property
    def ffmpeg_path(self) -> str:
        return self.ffmpeg

    @property
    def ffprobe_path(self) -> str:
        return self.ffprobe

    def version(self) -> str:

        result = subprocess.run(
            [self.ffmpeg, "-version"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.splitlines()[0]

    def execute(self, command: list[str]) -> subprocess.CompletedProcess:

        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

    def exists(self, file: Path) -> bool:

        return file.exists()

    def verify_video(self, video: Path) -> None:

        if not video.exists():
            raise FileNotFoundError(video)

    def execute_ffprobe(self, arguments: list[str]):

        command = [self.ffprobe]
        command.extend(arguments)

        return self.execute(command)

    def execute_ffmpeg(self, arguments: list[str]):

        command = [self.ffmpeg]
        command.extend(arguments)

        return self.execute(command)
