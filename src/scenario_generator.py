"""
Scenario generator: uses an LLM to derive test scenarios from video frames.
"""

from __future__ import annotations

import json
import re
from typing import List, Optional, Tuple

from .llm_client import LLMClient
from .models import Scenario


_SCENARIO_SYSTEM_PROMPT = """\
You are an expert QA analyst. You will be shown a series of video frames
(in chronological order) from a software application or product demo.

Your task is to analyse the visual content and produce a structured list of
*test scenarios* that a QA engineer should verify.

Rules:
- Identify every distinct user workflow, feature, or interaction shown.
- For each scenario provide: id, title, description, actors, preconditions,
  steps (ordered list of strings), expected_outcome, and tags.
- Use the id format "S-001", "S-002", etc.
- Return ONLY a valid JSON array of scenario objects. No markdown, no extra text.
"""

_SCENARIO_USER_TEMPLATE = """\
Below are {n} frames sampled from a video. Analyse them and return the scenarios.

Additional context provided by the user (may be empty):
{context}
"""


class ScenarioGeneratorError(Exception):
    """Raised when scenario generation fails."""


class ScenarioGenerator:
    """Generates test scenarios from a sequence of video frames.

    Parameters
    ----------
    llm_client:
        A configured :class:`~src.llm_client.LLMClient` instance.
    """

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm = llm_client

    def generate(
        self,
        frames: List[Tuple[float, str]],
        context: str = "",
    ) -> List[Scenario]:
        """Generate scenarios from sampled video frames.

        Parameters
        ----------
        frames:
            List of ``(timestamp_seconds, base64_jpeg)`` tuples as returned
            by :class:`~src.video_processor.VideoProcessor`.
        context:
            Optional free-text context about the video (e.g. product name,
            description of the workflow being demonstrated).

        Returns
        -------
        list of :class:`~src.models.Scenario` objects (without test cases).
        """
        if not frames:
            raise ScenarioGeneratorError("No frames provided for scenario generation.")

        b64_images = [b64 for _, b64 in frames]
        user_text = _SCENARIO_USER_TEMPLATE.format(
            n=len(b64_images),
            context=context or "(none)",
        )

        raw = self.llm.chat(
            system_prompt=_SCENARIO_SYSTEM_PROMPT,
            user_text=user_text,
            images=b64_images,
        )

        return self._parse_scenarios(raw)

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_scenarios(self, raw: str) -> List[Scenario]:
        """Parse the LLM response into a list of Scenario objects."""
        cleaned = self._extract_json(raw)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ScenarioGeneratorError(
                f"LLM did not return valid JSON for scenarios: {exc}\nRaw response:\n{raw}"
            ) from exc

        if not isinstance(data, list):
            raise ScenarioGeneratorError(
                f"Expected a JSON array of scenarios, got: {type(data).__name__}"
            )

        scenarios: List[Scenario] = []
        for i, item in enumerate(data):
            try:
                scenarios.append(Scenario(**item))
            except Exception as exc:
                raise ScenarioGeneratorError(
                    f"Failed to parse scenario at index {i}: {exc}\nData: {item}"
                ) from exc

        return scenarios

    @staticmethod
    def _extract_json(text: str) -> str:
        """Strip markdown code fences if present."""
        text = text.strip()
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            return match.group(1).strip()
        return text
