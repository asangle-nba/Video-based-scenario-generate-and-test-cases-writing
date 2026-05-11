"""
Test case writer: generates detailed test cases for each scenario using an LLM.
"""

from __future__ import annotations

import json
import re
from typing import List

from .llm_client import LLMClient
from .models import Scenario, TestCase, TestStep


_TEST_CASE_SYSTEM_PROMPT = """\
You are an expert QA engineer. Given a test scenario you will write detailed,
executable test cases in the standard Given-When-Then style.

Rules:
- Each test case must have: id, title, description, preconditions (list),
  steps (list of objects with step_number, action, expected_result),
  expected_outcome, priority (Low/Medium/High/Critical), and tags (list).
- Use id format "TC-001", "TC-002", etc. (continuing from the offset provided).
- Cover the happy path AND at least one negative / edge-case test per scenario.
- Return ONLY a valid JSON array of test case objects. No markdown, no extra text.
"""

_TEST_CASE_USER_TEMPLATE = """\
Scenario:
  id: {scenario_id}
  title: {scenario_title}
  description: {scenario_description}
  actors: {actors}
  preconditions: {preconditions}
  steps: {steps}
  expected_outcome: {expected_outcome}

Starting test case id offset: {id_offset}

Generate comprehensive test cases for this scenario.
"""


class TestCaseWriterError(Exception):
    """Raised when test case generation fails."""


class TestCaseWriter:
    """Generates detailed test cases from :class:`~src.models.Scenario` objects.

    Parameters
    ----------
    llm_client:
        A configured :class:`~src.llm_client.LLMClient` instance.
    """

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm = llm_client

    def write_test_cases(self, scenarios: List[Scenario]) -> List[Scenario]:
        """Populate each scenario's ``test_cases`` field.

        Parameters
        ----------
        scenarios:
            Scenarios previously returned by :class:`~src.scenario_generator.ScenarioGenerator`.

        Returns
        -------
        The same list of scenarios, each enriched with test cases.
        """
        tc_counter = 1
        for scenario in scenarios:
            test_cases = self._generate_for_scenario(scenario, id_offset=tc_counter)
            scenario.test_cases = test_cases
            tc_counter += len(test_cases)
        return scenarios

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _generate_for_scenario(
        self, scenario: Scenario, id_offset: int
    ) -> List[TestCase]:
        user_text = _TEST_CASE_USER_TEMPLATE.format(
            scenario_id=scenario.id,
            scenario_title=scenario.title,
            scenario_description=scenario.description,
            actors=", ".join(scenario.actors) or "N/A",
            preconditions=json.dumps(scenario.preconditions),
            steps=json.dumps(scenario.steps),
            expected_outcome=scenario.expected_outcome,
            id_offset=id_offset,
        )

        raw = self.llm.chat(
            system_prompt=_TEST_CASE_SYSTEM_PROMPT,
            user_text=user_text,
        )

        return self._parse_test_cases(raw)

    def _parse_test_cases(self, raw: str) -> List[TestCase]:
        cleaned = self._extract_json(raw)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise TestCaseWriterError(
                f"LLM did not return valid JSON for test cases: {exc}\nRaw response:\n{raw}"
            ) from exc

        if not isinstance(data, list):
            raise TestCaseWriterError(
                f"Expected a JSON array of test cases, got: {type(data).__name__}"
            )

        test_cases: List[TestCase] = []
        for i, item in enumerate(data):
            # Normalise nested steps
            if "steps" in item and isinstance(item["steps"], list):
                item["steps"] = [
                    s if isinstance(s, dict) else {"step_number": j + 1, "action": str(s), "expected_result": ""}
                    for j, s in enumerate(item["steps"])
                ]
            try:
                test_cases.append(TestCase(**item))
            except Exception as exc:
                raise TestCaseWriterError(
                    f"Failed to parse test case at index {i}: {exc}\nData: {item}"
                ) from exc

        return test_cases

    @staticmethod
    def _extract_json(text: str) -> str:
        """Strip markdown code fences if present."""
        text = text.strip()
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            return match.group(1).strip()
        return text
