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

        video_gen_result = self.services.generateVideo.encode_directory(
            input_directory=Path("./temp/jobs/20260714_115019/interpolated_frames"),
            output_directory=Path("./temp/jobs/20260714_115019/output/video.mp4"),
            fps=30
        )

        return PipelineResult(
            True,
            "Pipeline completed successfully.",
        )


