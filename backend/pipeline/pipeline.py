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

        job = manager.create_job()

        options = NCNNOptions(

            model_name="realesrgan-x4plus",

            scale=4,

            tile_size=512,

            gpu_id="auto",

            threads="1:2:2",

            output_format="webp",

            verbose=True,
        )

        self.services.enhancement.use_ncnn(

            executable=context.project_root / "models" / "realesrgan" / "realesrgan-ncnn-vulkan.exe",

            model_directory=context.project_root / "models" / "realesrgan" / "models",
        )

        self.logger.info(
            "Job created: %s",
            job.job_id,
        )

        #
        # Copy source video
        #

        input_video = copy_file(
            context.input_video,
            job.input / context.input_video.name,
        )

        #
        # Metadata
        #

        info = self.services.metadata.extract(input_video)

        with open(
                job.metadata,
                "w",
                encoding="utf-8",
        ) as file:

            json.dump(
                asdict(info),
                file,
                indent=4,
            )

        self.logger.info("Metadata extracted.")

        #
        # Audio
        #

        if self.services.audio.has_audio(input_video):

            audio_file = (
                    job.audio / "audio.aac"
            )

            self.services.audio.extract_audio(
                input_video,
                audio_file,
            )

            self.logger.info(
                "Audio extracted."
            )

        else:

            self.logger.info(
                "Video has no audio."
            )

        #
        # Frames
        #

        count = self.services.frames.extract(
            input_video=input_video,
            output_directory=job.frames,
            fps=5,
            image_format="jpg",
        )

        self.logger.info(
            "%d frames extracted.",
            count,
        )

        #
        # Preprocessing
        #

        processed = self.services.preprocessor.process_directory(
            input_directory=job.frames,
            output_directory=job.processed_frames,
            scale=0.25,  # Adjust extracted frames resolution and quality
            quality=90,
        )

        self.logger.info(
            "%d images processed.",
            processed,
        )

        result = self.services.enhancement.enhance_directory(

            input_directory=job.processed_frames,

            output_directory=job.enhanced_frames,

            options=options,
        )

        self.logger.info(

            "Enhancement completed using %s",

            result.model,
        )

        interpol_result = self.services.interpolation.interpolate_directory(
            input_directory=Path("./temp/jobs/20260714_115019/enhanced_frames"),
            output_directory=Path("./temp/jobs/20260714_115019/interpolated_frames"),
            options=RIFEOptions,
        )
        self.logger.info(

            "Frames Interpolation completed using %s",

            interpol_result.model,
        )

        outputDirectory = Path("./temp/jobs/20260714_115019/output")
        video_gen_result = self.services.generateVideo.encode_directory(
            input_directory=Path("./temp/jobs/20260714_115019/interpolated_frames"),
            output_video=outputDirectory / "video.mp4",
            fps=30
        )
        self.logger.info(

            "Video Reconstructed Successfully using %s",

            interpol_result.model,
        )

        return PipelineResult(
            True,
            "Pipeline completed successfully.",
        )


