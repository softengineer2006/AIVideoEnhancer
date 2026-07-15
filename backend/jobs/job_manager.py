from pathlib import Path

from backend.jobs.job import Job
from backend.utils.time_utils import current_timestamp


class JobManager:

    def __init__(self, temp_directory: Path):

        self.jobs_directory = temp_directory / "jobs"

        self.jobs_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_job(self) -> Job:

        job_id = current_timestamp()

        root = self.jobs_directory / job_id

        root.mkdir()

        folders = {

            "audio": root / "audio",

            "frames": root / "frames",

            "processed_frames": root / "processed_frames",

            "enhanced_frames": root / "enhanced_frames",

            "interpolated_frames": root / "interpolated_frames",

            "reconstructed": root / "reconstructed",

            "logs": root / "logs",

            "input": root / "input",

            "output": root / "output",
        }

        for folder in folders.values():
            folder.mkdir()

        return Job(

            job_id=job_id,

            root=root,

            metadata=root / "metadata.json",

            audio=folders["audio"],

            frames=folders["frames"],

            processed_frames=folders["processed_frames"],

            enhanced_frames=folders["enhanced_frames"],

            interpolated_frames=folders["interpolated_frames"],

            reconstructed=folders["reconstructed"],

            logs=folders["logs"],

            input=folders["input"],

            output=folders["output"],
        )
