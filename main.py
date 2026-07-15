from pathlib import Path

from backend.logging.logger import LoggerManager
from backend.pipeline.pipeline import VideoEnhancementPipeline
from backend.pipeline.pipeline_context import PipelineContext

PROJECT_ROOT = Path(__file__).resolve().parent


def main():

    LoggerManager(
        PROJECT_ROOT / "config" / "logging.yaml"
    ).setup()

    pipeline = VideoEnhancementPipeline()

    context = PipelineContext(

        project_root=PROJECT_ROOT,

        input_video=PROJECT_ROOT / "samples" / "sample.mp4",

        working_directory=PROJECT_ROOT / "temp",

        output_directory=PROJECT_ROOT / "output",
    )

    result = pipeline.run(context)

    print(result)


if __name__ == "__main__":
    main()
