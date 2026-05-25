"""
Data models for scenarios and test cases.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TestStep(BaseModel):
    step_number: int = Field(description="Ordered step number starting at 1")
    action: str = Field(description="The action to perform")
    expected_result: str = Field(description="The expected result of this action")


class TestCase(BaseModel):
    id: str = Field(description="Unique identifier, e.g. TC-001")
    title: str = Field(description="Short descriptive title of the test case")
    description: str = Field(description="Detailed description of what is being tested")
    preconditions: List[str] = Field(
        default_factory=list,
        description="Conditions that must be met before executing the test",
    )
    steps: List[TestStep] = Field(description="Ordered list of test steps")
    expected_outcome: str = Field(
        description="The overall expected outcome if all steps pass"
    )
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list, description="Labels for categorisation")


class Scenario(BaseModel):
    id: str = Field(description="Unique identifier, e.g. S-001")
    title: str = Field(description="Short descriptive title of the scenario")
    description: str = Field(description="What happens in this scenario")
    actors: List[str] = Field(
        default_factory=list,
        description="Entities (users, systems) involved in the scenario",
    )
    preconditions: List[str] = Field(default_factory=list)
    steps: List[str] = Field(description="High-level steps that make up the scenario")
    expected_outcome: str = Field(description="The expected result of the scenario")
    tags: List[str] = Field(default_factory=list)
    test_cases: List[TestCase] = Field(
        default_factory=list,
        description="Test cases derived from this scenario",
    )


class VideoAnalysisResult(BaseModel):
    video_path: str
    duration_seconds: Optional[float] = None
    frame_count: int = 0
    summary: str = Field(description="Plain-language summary of the video content")
    scenarios: List[Scenario] = Field(default_factory=list)
