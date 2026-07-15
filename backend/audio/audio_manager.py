from pathlib import Path

from backend.core.ffmpeg_manager import FFmpegManager
from backend.metadata.metadata_extractor import MetadataExtractor


class AudioManager:

    def __init__(self):

        self.ffmpeg = FFmpegManager()
        self.metadata = MetadataExtractor()

    def has_audio(self, video: Path) -> bool:

        info = self.metadata.extract(video)

        return info.audio_codec is not None

    def extract_audio(
        self,
        input_video: Path,
        output_audio: Path,
    ) -> Path:

        self.ffmpeg.verify_video(input_video)

        output_audio.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.ffmpeg.execute_ffmpeg([
            "-y",
            "-i",
            str(input_video),
            "-vn",
            "-acodec",
            "copy",
            str(output_audio),
        ])

        return output_audio

    def merge_audio(
            self,
            input_video: Path,
            input_audio: Path,
            output_video: Path,
    ) -> Path:
        self.ffmpeg.verify_video(input_video)

        if not input_audio.exists():
            raise FileNotFoundError(input_audio)

        output_video.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.ffmpeg.execute_ffmpeg([
            "-y",
            "-i",
            str(input_video),
            "-i",
            str(input_audio),
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            str(output_video),
        ])

        return output_video
