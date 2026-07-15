from dataclasses import dataclass


@dataclass(slots=True)
class RIFEOptions:

    target_fps: float = 30.0

    exp: int = 1

    device: str = "auto"

    # half: bool = False

    multi: int = 6

    verbose: bool = False
    