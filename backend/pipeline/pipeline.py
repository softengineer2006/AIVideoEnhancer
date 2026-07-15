import json
from dataclasses import asdict
from pathlib import Path

from backend.enhancement.ncnn_options import NCNNOptions
from backend.audio.audio_manager import AudioManager
from backend.extraction.frame_extractor import FrameExtractor
from backend.interpolation.rife_options import RIFEOptions
from backend.jobs.job_manager import JobManager
from backend.logging.logger import LoggerManager
from backend.metadata.metadata_extractor import MetadataExtractor
from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.pipeline_result import PipelineResult
from backend.preprocessing.image_preprocessor import ImagePreprocessor
from backend.services.media_services import MediaServices
from backend.utils.file_utils import copy_file


class VideoEnhancementPipeline:

    def __init__(self):
        self.logger = LoggerManager.get_logger("Pipeline")

        self.services = MediaServices()

    def run(
            self,
            context: PipelineContext,
    ) -> PipelineResult:

        manager = JobManager(
            context.working_directory
        )

        count = self.services.frames.extract(
            input_video=Path("./temp/jobs/20260714_115019/input/sample.mp4"),
            output_directory=Path("./temp/jobs/20260714_115019/frames_en/"),
            fps=5,
            image_format="jpg",
        )

        self.logger.info(
            "%d frames extracted.",
            count,
        )

        return PipelineResult(
            True,
            "Pipeline completed successfully.",
        )


