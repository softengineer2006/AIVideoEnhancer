from dataclasses import dataclass


@dataclass(slots=True)
class VideoMetadata:
    filename: str
    format_name: str

    duration: float
    size_bytes: int
    bit_rate: int

    width: int
    height: int

    fps: float
    total_frames: int

    video_codec: str
    pixel_format: str

    audio_codec: str | None
    sample_rate: int | None
    channels: int | None