from dataclasses import dataclass


@dataclass(slots=True)
class InterpolationResult:

    input_directory: str

    output_directory: str

    target_fps: float

    success: bool
    