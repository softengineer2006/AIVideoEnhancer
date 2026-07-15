from dataclasses import dataclass


@dataclass(slots=True)
class NCNNOptions:
    model_name: str = "realesrgan-x4plus"

    scale: int = 4

    tile_size: int = 0

    gpu_id: str = "auto"

    threads: str = "1:2:2"

    tta: bool = False

    output_format: str = "png"

    verbose: bool = False
