"""
Output formatter: converts VideoAnalysisResult into readable text / JSON.
"""

from __future__ import annotations

import json
from typing import Union

from .models import VideoAnalysisResult


class OutputFormatter:
    """Formats :class:`~src.models.VideoAnalysisResult` for display or export."""

    def to_json(self, result: VideoAnalysisResult, indent: int = 2) -> str:
        """Return the full result as a JSON string."""
        return result.model_dump_json(indent=indent)

    def to_markdown(self, result: VideoAnalysisResult) -> str:
        """Return a human-readable Markdown report."""
        lines = [
            f"# Video Analysis Report",
            f"",
            f"**Video:** `{result.video_path}`",
        ]
        if result.duration_seconds is not None:
            lines.append(f"**Duration:** {result.duration_seconds:.1f}s")
        lines += [
            f"**Frames analysed:** {result.frame_count}",
            f"",
            f"## Summary",
            f"",
            result.summary,
            f"",
            f"---",
            f"",
        ]

        for scenario in result.scenarios:
            lines += [
                f"## {scenario.id}: {scenario.title}",
                f"",
                f"**Description:** {scenario.description}",
                f"",
            ]
            if scenario.actors:
                lines.append(f"**Actors:** {', '.join(scenario.actors)}")
            if scenario.preconditions:
                lines.append(f"**Preconditions:**")
                for pc in scenario.preconditions:
                    lines.append(f"- {pc}")
            lines += [f"", f"**Steps:**"]
            for i, step in enumerate(scenario.steps, 1):
                lines.append(f"{i}. {step}")
            lines += [f"", f"**Expected outcome:** {scenario.expected_outcome}", f""]

            if scenario.test_cases:
                lines += [f"### Test Cases", f""]
                for tc in scenario.test_cases:
                    lines += [
                        f"#### {tc.id}: {tc.title}",
                        f"",
                        f"- **Priority:** {tc.priority.value}",
                        f"- **Description:** {tc.description}",
                    ]
                    if tc.preconditions:
                        lines.append(f"- **Preconditions:** {'; '.join(tc.preconditions)}")
                    lines += [f"", f"| Step | Action | Expected Result |", f"|------|--------|-----------------|"]
                    for step in tc.steps:
                        lines.append(
                            f"| {step.step_number} | {step.action} | {step.expected_result} |"
                        )
                    lines += [
                        f"",
                        f"**Expected outcome:** {tc.expected_outcome}",
                        f"",
                    ]

        return "\n".join(lines)
