"""
Main entry point for the Video Scenario & Test Case Generator.

Usage
-----
    python -m src.main --video path/to/video.mp4

Or after installing the package:
    video-scenario-gen --video path/to/video.mp4
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

load_dotenv()

from .llm_client import LLMClient
from .models import VideoAnalysisResult
from .output_formatter import OutputFormatter
from .scenario_generator import ScenarioGenerator
from .test_case_writer import TestCaseWriter
from .video_processor import VideoProcessor


@click.command()
@click.option(
    "--video",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the input video file.",
)
@click.option(
    "--context",
    default="",
    help="Optional free-text description of the video to guide the LLM.",
)
@click.option(
    "--provider",
    default=None,
    help="LLM provider: 'openai' or 'gemini'. Defaults to LLM_PROVIDER env var or 'openai'.",
)
@click.option(
    "--model",
    default=None,
    help="LLM model name. Defaults to the provider's recommended model.",
)
@click.option(
    "--fps",
    default=None,
    type=float,
    help="Frames per second to sample. Defaults to FRAMES_PER_SECOND env var or 1.",
)
@click.option(
    "--max-frames",
    default=None,
    type=int,
    help="Maximum number of frames to send to the LLM. Defaults to MAX_FRAMES env var or 50.",
)
@click.option(
    "--output",
    default=None,
    type=click.Path(dir_okay=False, writable=True),
    help="Output file path. If omitted, prints to stdout.",
)
@click.option(
    "--format",
    "output_format",
    default="markdown",
    type=click.Choice(["markdown", "json"], case_sensitive=False),
    help="Output format (default: markdown).",
)
@click.option(
    "--skip-test-cases",
    is_flag=True,
    default=False,
    help="Generate scenarios only, without writing test cases.",
)
def main(
    video: str,
    context: str,
    provider: str | None,
    model: str | None,
    fps: float | None,
    max_frames: int | None,
    output: str | None,
    output_format: str,
    skip_test_cases: bool,
) -> None:
    """Generate test scenarios and test cases from a video file using an LLM."""
    # ── Configuration ──────────────────────────────────────────────────
    provider = provider or os.environ.get("LLM_PROVIDER", "openai")
    fps = fps or float(os.environ.get("FRAMES_PER_SECOND", "1"))
    max_frames = max_frames or int(os.environ.get("MAX_FRAMES", "50"))
    frame_width = int(os.environ.get("FRAME_WIDTH", "1280"))

    click.echo(f"[1/4] Processing video: {video}", err=True)

    # ── Video processing ────────────────────────────────────────────────
    processor = VideoProcessor(
        frames_per_second=fps,
        max_frames=max_frames,
        frame_width=frame_width,
    )
    metadata = processor.get_video_metadata(video)
    frames = processor.extract_frames(video)
    click.echo(
        f"      Extracted {len(frames)} frames from "
        f"{metadata['duration_seconds']:.1f}s video.",
        err=True,
    )

    # ── LLM client ──────────────────────────────────────────────────────
    llm = LLMClient(provider=provider, model=model)

    # ── Scenario generation ─────────────────────────────────────────────
    click.echo(f"[2/4] Generating scenarios with {provider}/{llm.model} …", err=True)
    generator = ScenarioGenerator(llm_client=llm)
    scenarios = generator.generate(frames=frames, context=context)
    click.echo(f"      Found {len(scenarios)} scenario(s).", err=True)

    # ── Test case writing ───────────────────────────────────────────────
    if not skip_test_cases:
        click.echo(f"[3/4] Writing test cases …", err=True)
        writer = TestCaseWriter(llm_client=llm)
        scenarios = writer.write_test_cases(scenarios)
        total_tc = sum(len(s.test_cases) for s in scenarios)
        click.echo(f"      Generated {total_tc} test case(s).", err=True)
    else:
        click.echo(f"[3/4] Skipping test case generation (--skip-test-cases).", err=True)

    # ── Assemble result ─────────────────────────────────────────────────
    result = VideoAnalysisResult(
        video_path=video,
        duration_seconds=metadata["duration_seconds"],
        frame_count=len(frames),
        summary=f"Analysed {len(frames)} frames; identified {len(scenarios)} scenario(s).",
        scenarios=scenarios,
    )

    # ── Format & output ─────────────────────────────────────────────────
    click.echo(f"[4/4] Formatting output ({output_format}) …", err=True)
    formatter = OutputFormatter()
    if output_format == "json":
        text = formatter.to_json(result)
    else:
        text = formatter.to_markdown(result)

    if output:
        Path(output).write_text(text, encoding="utf-8")
        click.echo(f"      Output written to: {output}", err=True)
    else:
        click.echo(text)


if __name__ == "__main__":
    main()
