import json
from fractions import Fraction
from pathlib import Path

from backend.core.ffmpeg_manager import FFmpegManager
from backend.metadata.models import VideoMetadata


class MetadataExtractor:

    def __init__(self):

        self.ffmpeg = FFmpegManager()

    @staticmethod
    def _fps(value: str) -> float:

        try:
            return float(Fraction(value))
        except Exception:
            return 0.0

    def extract(self, video: Path) -> VideoMetadata:

        self.ffmpeg.verify_video(video)

        result = self.ffmpeg.execute_ffprobe([
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video),
        ])

        data = json.loads(result.stdout)

        streams = data["streams"]

        format_data = data["format"]

        video_stream = next(
            s for s in streams if s["codec_type"] == "video"
        )

        audio_stream = next(
            (
                s
                for s in streams
                if s["codec_type"] == "audio"
            ),
            None,
        )

        fps = self._fps(video_stream["avg_frame_rate"])

        duration = float(format_data.get("duration", 0))

        total_frames = int(duration * fps)

        return VideoMetadata(
            filename=video.name,

            format_name=format_data.get("format_name", ""),

            duration=duration,

            size_bytes=int(format_data.get("size", 0)),

            bit_rate=int(format_data.get("bit_rate", 0)),

            width=int(video_stream["width"]),

            height=int(video_stream["height"]),

            fps=fps,

            total_frames=total_frames,

            video_codec=video_stream.get("codec_name", ""),

            pixel_format=video_stream.get("pix_fmt", ""),

            audio_codec=(
                audio_stream.get("codec_name")
                if audio_stream
                else None
            ),

            sample_rate=(
                int(audio_stream["sample_rate"])
                if audio_stream
                else None
            ),

            channels=(
                int(audio_stream["channels"])
                if audio_stream
                else None
            ),
        )