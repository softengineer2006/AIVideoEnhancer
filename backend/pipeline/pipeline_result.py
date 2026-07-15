from dataclasses import dataclass


@dataclass(slots=True)
class PipelineResult:

    success: bool

    message: str
