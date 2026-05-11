"""
Tests for OutputFormatter.
"""

from __future__ import annotations

import json

import pytest

from src.models import Priority, Scenario, TestCase, TestStep, VideoAnalysisResult
from src.output_formatter import OutputFormatter


def _make_result(with_test_cases: bool = True) -> VideoAnalysisResult:
    steps = [
        TestStep(step_number=1, action="Open app", expected_result="App opens"),
        TestStep(step_number=2, action="Click login", expected_result="Login form shown"),
    ]
    tc = TestCase(
        id="TC-001",
        title="Login happy path",
        description="Test successful login",
        preconditions=["User is registered"],
        steps=steps,
        expected_outcome="User lands on dashboard",
        priority=Priority.HIGH,
        tags=["auth"],
    )
    scenario = Scenario(
        id="S-001",
        title="User Login",
        description="Login flow",
        actors=["User"],
        preconditions=["App running"],
        steps=["Open app", "Enter credentials", "Click Login"],
        expected_outcome="Dashboard shown",
        tags=["auth"],
        test_cases=[tc] if with_test_cases else [],
    )
    return VideoAnalysisResult(
        video_path="demo.mp4",
        duration_seconds=30.0,
        frame_count=15,
        summary="Video shows a login flow.",
        scenarios=[scenario],
    )


class TestOutputFormatter:
    def setup_method(self):
        self.formatter = OutputFormatter()

    def test_to_json_is_valid(self):
        result = _make_result()
        output = self.formatter.to_json(result)
        parsed = json.loads(output)
        assert parsed["video_path"] == "demo.mp4"
        assert len(parsed["scenarios"]) == 1

    def test_to_json_includes_test_cases(self):
        result = _make_result(with_test_cases=True)
        output = self.formatter.to_json(result)
        parsed = json.loads(output)
        assert len(parsed["scenarios"][0]["test_cases"]) == 1

    def test_to_markdown_contains_scenario(self):
        result = _make_result()
        md = self.formatter.to_markdown(result)
        assert "S-001" in md
        assert "User Login" in md
        assert "TC-001" in md

    def test_to_markdown_contains_summary(self):
        result = _make_result()
        md = self.formatter.to_markdown(result)
        assert "Video shows a login flow" in md

    def test_to_markdown_contains_duration(self):
        result = _make_result()
        md = self.formatter.to_markdown(result)
        assert "30.0" in md

    def test_to_markdown_without_test_cases(self):
        result = _make_result(with_test_cases=False)
        md = self.formatter.to_markdown(result)
        assert "S-001" in md
        assert "TC-001" not in md
