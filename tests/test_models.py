"""
Tests for data models.
"""

import pytest
from pydantic import ValidationError

from src.models import Priority, Scenario, TestCase, TestStep, VideoAnalysisResult


class TestTestStep:
    def test_basic(self):
        step = TestStep(step_number=1, action="Click Login", expected_result="Login page opens")
        assert step.step_number == 1
        assert step.action == "Click Login"

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            TestStep(step_number=1)  # missing action and expected_result


class TestTestCase:
    def test_basic(self):
        tc = TestCase(
            id="TC-001",
            title="Login with valid credentials",
            description="Verify successful login",
            steps=[TestStep(step_number=1, action="Enter username", expected_result="Field populated")],
            expected_outcome="User is logged in",
        )
        assert tc.id == "TC-001"
        assert tc.priority == Priority.MEDIUM  # default

    def test_priority_enum(self):
        tc = TestCase(
            id="TC-002",
            title="t",
            description="d",
            steps=[TestStep(step_number=1, action="a", expected_result="e")],
            expected_outcome="o",
            priority=Priority.HIGH,
        )
        assert tc.priority == Priority.HIGH


class TestScenario:
    def test_basic(self):
        s = Scenario(
            id="S-001",
            title="User login",
            description="A user logs in",
            steps=["Navigate to login page", "Enter credentials", "Click submit"],
            expected_outcome="User lands on dashboard",
        )
        assert s.id == "S-001"
        assert len(s.steps) == 3
        assert s.test_cases == []

    def test_with_test_cases(self):
        tc = TestCase(
            id="TC-001",
            title="t",
            description="d",
            steps=[TestStep(step_number=1, action="a", expected_result="e")],
            expected_outcome="o",
        )
        s = Scenario(
            id="S-001",
            title="t",
            description="d",
            steps=["step 1"],
            expected_outcome="outcome",
            test_cases=[tc],
        )
        assert len(s.test_cases) == 1


class TestVideoAnalysisResult:
    def test_basic(self):
        r = VideoAnalysisResult(video_path="test.mp4", summary="A test video", frame_count=10)
        assert r.video_path == "test.mp4"
        assert r.scenarios == []
        assert r.duration_seconds is None
