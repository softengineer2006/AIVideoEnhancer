from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PipelineContext:

    project_root: Path

    input_video: Path

    working_directory: Path

    output_directory: Path
