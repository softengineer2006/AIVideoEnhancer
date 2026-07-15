from pathlib import Path

import cv2
import numpy as np

from backend.core.ffmpeg_manager import FFmpegManager


class FrameExtractor:
    """
    Extracts a fixed number of frames per second from a video.

    Rather than sampling at evenly-spaced time intervals, for every
    1-second window of source video this scores every frame in that
    window by visual detail (entropy) and motion / scene-change
    likelihood, then keeps the top `fps` most "important" frames from
    that window. Hard scene changes are always prioritized so cuts
    aren't missed, but the total number of frames kept per second is
    always exactly `fps` (or fewer only if the window itself has fewer
    frames than that, e.g. the last partial second of the video).
    """

    def __init__(self) -> None:
        self.ffmpeg = FFmpegManager()

    @staticmethod
    def _frame_entropy(gray_frame: np.ndarray) -> float:
        """
        Shannon entropy (in bits, 0-8) of the frame's grayscale
        histogram. Higher = more visual detail / texture.
        """

        histogram = cv2.calcHist([gray_frame], [0], None, [256], [0, 256])
        histogram = histogram.ravel() / (histogram.sum() + 1e-8)

        nonzero = histogram[histogram > 0]

        entropy = float(-np.sum(nonzero * np.log2(nonzero)))

        return entropy

    @staticmethod
    def _motion_score(gray_frame: np.ndarray, prev_gray_frame: np.ndarray | None) -> float:
        """
        Normalized (0-1) mean absolute pixel difference against the
        previous frame. Higher = more motion / more likely a scene change.
        """

        if prev_gray_frame is None:
            return 0.0

        diff = cv2.absdiff(gray_frame, prev_gray_frame)

        return float(diff.mean()) / 255.0

    def extract(
        self,
        input_video: Path,
        output_directory: Path,
        fps: float = 5.0,
        image_format: str = "jpg",
        scene_change_threshold: float = 0.35,
        entropy_weight: float = 0.5,
        motion_weight: float = 0.5,
    ) -> int:
        """
        Extracts exactly `fps` frames per second of `input_video` into
        `output_directory`, choosing which frames to keep based on
        entropy and scene-change / motion scoring.

        For every 1-second window of source video:
          - each frame's entropy and inter-frame motion score are
            combined into a single 0-1 importance score
          - frames whose motion score exceeds `scene_change_threshold`
            are treated as hard scene changes and are prioritized first
          - the remaining budget (up to `fps` total for that window) is
            filled by the highest-scoring frames

        Returns the total number of frames written.
        """

        self.ffmpeg.verify_video(input_video)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        image_format = image_format.lower()

        if image_format not in ("png", "jpg", "webp"):
            raise ValueError(
                "image_format must be 'png' or 'jpg' or 'webp'"
            )

        for image in output_directory.glob("*"):
            if image.is_file():
                image.unlink()

        if fps <= 0:
            raise ValueError("fps must be positive.")

        capture = cv2.VideoCapture(str(input_video))

        if not capture.isOpened():
            raise ValueError(f"Unable to open video: {input_video}")

        source_fps = capture.get(cv2.CAP_PROP_FPS) or 30.0

        if source_fps <= 0:
            source_fps = 30.0

        window_size = max(int(round(source_fps)), 1)

        # How many frames to keep per 1-second window. Cannot exceed the
        # number of source frames actually available in that window.
        frames_per_window = max(1, int(round(fps)))

        saved_count = 0

        def flush_window(frames: list[tuple[np.ndarray, float, float, bool]]) -> None:
            nonlocal saved_count

            if not frames:
                return

            scores = [
                entropy_weight * (entropy / 8.0) + motion_weight * motion
                for (_, entropy, motion, _) in frames
            ]

            budget = min(frames_per_window, len(frames))

            forced_indices = [
                index for index, (_, _, _, is_scene_change)
                in enumerate(frames)
                if is_scene_change
            ]

            # If more scene changes were detected than the budget allows,
            # keep only the highest-scoring ones among them.
            forced_indices.sort(key=lambda index: scores[index], reverse=True)
            chosen = set(forced_indices[:budget])

            ranked_indices = sorted(
                range(len(frames)),
                key=lambda index: scores[index],
                reverse=True,
            )

            for index in ranked_indices:
                if len(chosen) >= budget:
                    break
                chosen.add(index)

            for index in sorted(chosen):
                image, _, _, _ = frames[index]

                filename = (
                    output_directory
                    / f"frame_{saved_count:06d}.{image_format}"
                )

                cv2.imwrite(str(filename), image)

                saved_count += 1

        window_frames: list[tuple[np.ndarray, float, float, bool]] = []
        prev_gray = None

        while True:

            ok, frame = capture.read()

            if not ok:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            entropy = self._frame_entropy(gray)
            motion = self._motion_score(gray, prev_gray)
            is_scene_change = motion > scene_change_threshold

            window_frames.append((frame, entropy, motion, is_scene_change))

            prev_gray = gray

            if len(window_frames) >= window_size:
                flush_window(window_frames)
                window_frames = []

        flush_window(window_frames)

        capture.release()

        return saved_count