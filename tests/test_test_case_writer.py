"""
Tests for TestCaseWriter (mocked LLM).
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.test_case_writer import TestCaseWriter, TestCaseWriterError
from src.models import Scenario, TestCase


SAMPLE_TEST_CASES_JSON = json.dumps(
    [
        {
            "id": "TC-001",
            "title": "Login with valid credentials",
            "description": "Verify a registered user can log in with correct credentials",
            "preconditions": ["User has registered account", "App is running"],
            "steps": [
                {"step_number": 1, "action": "Open the app", "expected_result": "Login page is displayed"},
                {"step_number": 2, "action": "Enter valid username", "expected_result": "Username field is populated"},
                {"step_number": 3, "action": "Enter valid password", "expected_result": "Password field is masked"},
                {"step_number": 4, "action": "Click Login button", "expected_result": "Dashboard is displayed"},
            ],
            "expected_outcome": "User is successfully logged in and sees dashboard",
            "priority": "High",
            "tags": ["auth", "happy-path"],
        },
        {
            "id": "TC-002",
            "title": "Login with invalid credentials",
            "description": "Verify appropriate error when invalid credentials are used",
            "preconditions": ["App is running"],
            "steps": [
                {"step_number": 1, "action": "Open the app", "expected_result": "Login page is displayed"},
                {"step_number": 2, "action": "Enter invalid username", "expected_result": "Username field populated"},
                {"step_number": 3, "action": "Enter invalid password", "expected_result": "Password field masked"},
                {"step_number": 4, "action": "Click Login button", "expected_result": "Error message displayed"},
            ],
            "expected_outcome": "User sees an error and is not logged in",
            "priority": "High",
            "tags": ["auth", "negative"],
        },
    ]
)


def _make_scenario() -> Scenario:
    return Scenario(
        id="S-001",
        title="User Login",
        description="A user logs in",
        actors=["User"],
        preconditions=["User has account"],
        steps=["Open app", "Enter credentials", "Click Login"],
        expected_outcome="User on dashboard",
    )


class TestTestCaseWriter:
    def _make_writer(self, llm_response: str) -> TestCaseWriter:
        mock_llm = MagicMock()
        mock_llm.chat.return_value = llm_response
        return TestCaseWriter(llm_client=mock_llm)

    def test_write_test_cases_populates_scenarios(self):
        writer = self._make_writer(SAMPLE_TEST_CASES_JSON)
        scenarios = [_make_scenario()]
        result = writer.write_test_cases(scenarios)
        assert len(result) == 1
        assert len(result[0].test_cases) == 2
        assert isinstance(result[0].test_cases[0], TestCase)

    def test_test_case_fields(self):
        writer = self._make_writer(SAMPLE_TEST_CASES_JSON)
        result = writer.write_test_cases([_make_scenario()])
        tc = result[0].test_cases[0]
        assert tc.id == "TC-001"
        assert tc.title == "Login with valid credentials"
        assert len(tc.steps) == 4
        assert tc.steps[0].step_number == 1

    def test_multiple_scenarios_get_test_cases(self):
        writer = self._make_writer(SAMPLE_TEST_CASES_JSON)
        s1 = _make_scenario()
        s2 = Scenario(
            id="S-002",
            title="Search",
            description="User searches",
            steps=["Type query", "Press enter"],
            expected_outcome="Results shown",
        )
        result = writer.write_test_cases([s1, s2])
        assert all(len(s.test_cases) == 2 for s in result)

    def test_raises_on_invalid_json(self):
        writer = self._make_writer("not valid json")
        with pytest.raises(TestCaseWriterError, match="valid JSON"):
            writer.write_test_cases([_make_scenario()])

    def test_raises_on_non_array(self):
        writer = self._make_writer('{"id": "TC-001"}')
        with pytest.raises(TestCaseWriterError, match="JSON array"):
            writer.write_test_cases([_make_scenario()])

    def test_strips_markdown_fences(self):
        wrapped = f"```json\n{SAMPLE_TEST_CASES_JSON}\n```"
        writer = self._make_writer(wrapped)
        result = writer.write_test_cases([_make_scenario()])
        assert len(result[0].test_cases) == 2
