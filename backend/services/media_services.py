from pathlib import Path

from backend.audio.audio_manager import AudioManager
from backend.enhancement.enhancement_engine import EnhancementEngine
from backend.extraction.frame_extractor import FrameExtractor
from backend.metadata.metadata_extractor import MetadataExtractor
from backend.preprocessing.image_preprocessor import ImagePreprocessor
from backend.interpolation.interpolation_engine import (
    InterpolationEngine,
)
from backend.pipeline.pipeline_context import PipelineContext


class MediaServices:
    """
    Holds long-lived service instances used by the pipeline.
    """

    def __init__(self):

        self.metadata = MetadataExtractor()

        self.audio = AudioManager()

        self.frames = FrameExtractor()

        self.preprocessor = ImagePreprocessor()

        self.enhancement = EnhancementEngine()

        self.interpolation = InterpolationEngine()

        self.interpolation.use_rife(

            repository_path=Path("./third_party/Practical-RIFE"),

            model_directory=Path("./third_party/Practical-RIFE/train_log")
        )
