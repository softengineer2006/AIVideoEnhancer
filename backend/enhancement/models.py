from dataclasses import dataclass


@dataclass(slots=True)
class EnhancementResult:
    input_directory: str
    output_directory: str

    model: str

    scale: int

    success: bool