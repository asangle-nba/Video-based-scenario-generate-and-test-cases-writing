"""
Video processor: extracts frames from a video file for downstream LLM analysis.
"""

from __future__ import annotations

import base64
import io
import os
from pathlib import Path
from typing import List, Tuple

try:
    import cv2  # type: ignore
    _CV2_AVAILABLE = True
except ImportError:  # pragma: no cover
    _CV2_AVAILABLE = False

try:
    from PIL import Image  # type: ignore
    _PIL_AVAILABLE = True
except ImportError:  # pragma: no cover
    _PIL_AVAILABLE = False


class VideoProcessorError(Exception):
    """Raised when video processing fails."""


class VideoProcessor:
    """Extracts a representative sample of frames from a video file."""

    def __init__(
        self,
        frames_per_second: float = 1.0,
        max_frames: int = 50,
        frame_width: int = 1280,
    ) -> None:
        if not _CV2_AVAILABLE:
            raise VideoProcessorError(
                "opencv-python-headless is required: pip install opencv-python-headless"
            )
        if not _PIL_AVAILABLE:
            raise VideoProcessorError(
                "Pillow is required: pip install Pillow"
            )
        self.frames_per_second = frames_per_second
        self.max_frames = max_frames
        self.frame_width = frame_width

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_frames(self, video_path: str | Path) -> List[Tuple[float, str]]:
        """Extract frames and return a list of ``(timestamp_sec, base64_jpeg)`` tuples.

        Parameters
        ----------
        video_path:
            Path to the local video file.

        Returns
        -------
        list of (timestamp_seconds, base64_encoded_jpeg_string)
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise VideoProcessorError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise VideoProcessorError(f"Could not open video: {video_path}")

        try:
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps

            sample_interval = max(1, int(fps / self.frames_per_second))
            frame_indices = list(range(0, total_frames, sample_interval))

            if len(frame_indices) > self.max_frames:
                step = len(frame_indices) // self.max_frames
                frame_indices = frame_indices[::step][: self.max_frames]

            results: List[Tuple[float, str]] = []
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue
                timestamp = idx / fps
                b64 = self._encode_frame(frame)
                results.append((timestamp, b64))

            return results
        finally:
            cap.release()

    def get_video_metadata(self, video_path: str | Path) -> dict:
        """Return basic metadata about a video file."""
        video_path = Path(video_path)
        if not video_path.exists():
            raise VideoProcessorError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise VideoProcessorError(f"Could not open video: {video_path}")

        try:
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = total_frames / fps
            return {
                "fps": fps,
                "total_frames": total_frames,
                "duration_seconds": duration,
                "width": width,
                "height": height,
            }
        finally:
            cap.release()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _encode_frame(self, bgr_frame) -> str:
        """Convert a BGR OpenCV frame to a base64-encoded JPEG string."""
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        if pil_img.width > self.frame_width:
            ratio = self.frame_width / pil_img.width
            new_height = int(pil_img.height * ratio)
            pil_img = pil_img.resize(
                (self.frame_width, new_height), Image.Resampling.LANCZOS
            )

        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
