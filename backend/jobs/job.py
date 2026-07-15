from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Job:

    job_id: str

    root: Path

    metadata: Path

    audio: Path

    frames: Path

    processed_frames: Path

    enhanced_frames: Path

    interpolated_frames: Path

    reconstructed: Path

    logs: Path

    input: Path

    output: Path
