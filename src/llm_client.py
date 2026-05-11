"""
LLM client abstraction that supports OpenAI (gpt-4o) and Google Gemini.
"""

from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict, List, Optional, Tuple


class LLMClientError(Exception):
    """Raised when an LLM API call fails."""


class LLMClient:
    """Provider-agnostic LLM wrapper for multimodal (text + image) calls.

    Parameters
    ----------
    provider:
        ``"openai"`` or ``"gemini"``.
    api_key:
        API key for the chosen provider. Falls back to the corresponding
        environment variable when *None*.
    model:
        Model name to use. Defaults to ``"gpt-4o"`` for OpenAI and
        ``"gemini-1.5-pro"`` for Gemini.
    """

    OPENAI_DEFAULT_MODEL = "gpt-4o"
    GEMINI_DEFAULT_MODEL = "gemini-1.5-pro"

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.provider = provider.lower()
        if self.provider not in ("openai", "gemini"):
            raise LLMClientError(f"Unsupported provider: {provider!r}. Choose 'openai' or 'gemini'.")

        self.api_key = api_key or self._env_key()
        self.model = model or self._default_model()
        self._client: Any = None  # lazily initialised

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(
        self,
        system_prompt: str,
        user_text: str,
        images: Optional[List[str]] = None,
        response_format: Optional[Dict] = None,
    ) -> str:
        """Send a (multimodal) chat request and return the text response.

        Parameters
        ----------
        system_prompt:
            The system-level instruction.
        user_text:
            The user message text.
        images:
            Optional list of base64-encoded JPEG strings to attach.
        response_format:
            Optional JSON schema for structured output (OpenAI only).
        """
        if self.provider == "openai":
            return self._openai_chat(system_prompt, user_text, images, response_format)
        return self._gemini_chat(system_prompt, user_text, images)

    # ------------------------------------------------------------------
    # OpenAI
    # ------------------------------------------------------------------

    def _openai_chat(
        self,
        system_prompt: str,
        user_text: str,
        images: Optional[List[str]],
        response_format: Optional[Dict],
    ) -> str:
        client = self._get_openai_client()

        user_content: List[Any] = [{"type": "text", "text": user_text}]
        if images:
            for b64 in images:
                user_content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64}",
                            "detail": "low",
                        },
                    }
                )

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "max_tokens": 4096,
        }
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as exc:
            raise LLMClientError(f"OpenAI API error: {exc}") from exc

    def _get_openai_client(self):
        if self._client is None:
            try:
                from openai import OpenAI  # type: ignore
            except ImportError as exc:
                raise LLMClientError(
                    "openai package is required: pip install openai"
                ) from exc
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    # ------------------------------------------------------------------
    # Gemini
    # ------------------------------------------------------------------

    def _gemini_chat(
        self,
        system_prompt: str,
        user_text: str,
        images: Optional[List[str]],
    ) -> str:
        try:
            import google.generativeai as genai  # type: ignore
        except ImportError as exc:
            raise LLMClientError(
                "google-generativeai package is required: pip install google-generativeai"
            ) from exc

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=system_prompt,
        )

        parts: List[Any] = [user_text]
        if images:
            try:
                from PIL import Image  # type: ignore
                import io

                for b64 in images:
                    img_bytes = base64.b64decode(b64)
                    pil_img = Image.open(io.BytesIO(img_bytes))
                    parts.append(pil_img)
            except ImportError as exc:
                raise LLMClientError(
                    "Pillow is required for Gemini image support: pip install Pillow"
                ) from exc

        try:
            response = model.generate_content(parts)
            return response.text or ""
        except Exception as exc:
            raise LLMClientError(f"Gemini API error: {exc}") from exc

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _env_key(self) -> str:
        if self.provider == "openai":
            key = os.environ.get("OPENAI_API_KEY", "")
        else:
            key = os.environ.get("GOOGLE_API_KEY", "")
        return key

    def _default_model(self) -> str:
        if self.provider == "openai":
            return self.OPENAI_DEFAULT_MODEL
        return self.GEMINI_DEFAULT_MODEL
