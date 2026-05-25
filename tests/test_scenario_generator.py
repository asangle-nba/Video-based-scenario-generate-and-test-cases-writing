"""
Tests for ScenarioGenerator (mocked LLM).
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from src.scenario_generator import ScenarioGenerator, ScenarioGeneratorError
from src.models import Scenario


SAMPLE_SCENARIOS_JSON = json.dumps(
    [
        {
            "id": "S-001",
            "title": "User Login",
            "description": "A user logs into the application",
            "actors": ["Registered User"],
            "preconditions": ["User has an account"],
            "steps": ["Open the app", "Enter credentials", "Click Login"],
            "expected_outcome": "User is on the dashboard",
            "tags": ["auth", "login"],
        }
    ]
)


class TestScenarioGenerator:
    def _make_generator(self, llm_response: str) -> ScenarioGenerator:
        mock_llm = MagicMock()
        mock_llm.chat.return_value = llm_response
        return ScenarioGenerator(llm_client=mock_llm)

    def test_generate_returns_scenarios(self):
        gen = self._make_generator(SAMPLE_SCENARIOS_JSON)
        frames = [(0.0, "base64data"), (1.0, "base64data2")]
        scenarios = gen.generate(frames=frames)
        assert len(scenarios) == 1
        assert isinstance(scenarios[0], Scenario)
        assert scenarios[0].id == "S-001"
        assert scenarios[0].title == "User Login"

    def test_generate_strips_markdown_fences(self):
        wrapped = f"```json\n{SAMPLE_SCENARIOS_JSON}\n```"
        gen = self._make_generator(wrapped)
        scenarios = gen.generate(frames=[(0.0, "b64")])
        assert len(scenarios) == 1

    def test_generate_with_context(self):
        mock_llm = MagicMock()
        mock_llm.chat.return_value = SAMPLE_SCENARIOS_JSON
        gen = ScenarioGenerator(llm_client=mock_llm)
        gen.generate(frames=[(0.0, "b64")], context="Login flow demo")
        call_kwargs = mock_llm.chat.call_args
        assert "Login flow demo" in call_kwargs.kwargs.get("user_text", "") or \
               "Login flow demo" in str(call_kwargs)

    def test_generate_raises_on_empty_frames(self):
        gen = self._make_generator(SAMPLE_SCENARIOS_JSON)
        with pytest.raises(ScenarioGeneratorError):
            gen.generate(frames=[])

    def test_generate_raises_on_invalid_json(self):
        gen = self._make_generator("not json at all")
        with pytest.raises(ScenarioGeneratorError, match="valid JSON"):
            gen.generate(frames=[(0.0, "b64")])

    def test_generate_raises_on_non_array_json(self):
        gen = self._make_generator('{"id": "S-001"}')
        with pytest.raises(ScenarioGeneratorError, match="JSON array"):
            gen.generate(frames=[(0.0, "b64")])

    def test_extract_json_no_fences(self):
        raw = '  [{"id":"S-001"}]  '
        result = ScenarioGenerator._extract_json(raw)
        assert result == '[{"id":"S-001"}]'

    def test_extract_json_with_fences(self):
        raw = "```json\n[1, 2, 3]\n```"
        result = ScenarioGenerator._extract_json(raw)
        assert result == "[1, 2, 3]"
