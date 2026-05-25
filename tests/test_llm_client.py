"""
Tests for LLMClient.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.llm_client import LLMClient, LLMClientError


class TestLLMClientInit:
    def test_default_provider_is_openai(self):
        client = LLMClient()
        assert client.provider == "openai"
        assert client.model == LLMClient.OPENAI_DEFAULT_MODEL

    def test_gemini_provider(self):
        client = LLMClient(provider="gemini")
        assert client.provider == "gemini"
        assert client.model == LLMClient.GEMINI_DEFAULT_MODEL

    def test_custom_model(self):
        client = LLMClient(provider="openai", model="gpt-4-turbo")
        assert client.model == "gpt-4-turbo"

    def test_invalid_provider_raises(self):
        with pytest.raises(LLMClientError, match="Unsupported provider"):
            LLMClient(provider="anthropic")

    def test_api_key_from_param(self):
        client = LLMClient(api_key="sk-test-key")
        assert client.api_key == "sk-test-key"

    def test_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "env-key-123")
        client = LLMClient(provider="openai")
        assert client.api_key == "env-key-123"


class TestLLMClientOpenAI:
    def test_chat_calls_openai(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello from OpenAI"

        mock_openai = MagicMock()
        mock_openai.chat.completions.create.return_value = mock_response

        client = LLMClient(provider="openai", api_key="sk-test")
        client._client = mock_openai

        result = client.chat(system_prompt="You are helpful.", user_text="Hi")
        assert result == "Hello from OpenAI"
        mock_openai.chat.completions.create.assert_called_once()

    def test_chat_with_images(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "I see an image"

        mock_openai = MagicMock()
        mock_openai.chat.completions.create.return_value = mock_response

        client = LLMClient(provider="openai", api_key="sk-test")
        client._client = mock_openai

        result = client.chat(
            system_prompt="You are a vision model.",
            user_text="Describe this",
            images=["base64encodedimage"],
        )
        assert result == "I see an image"
        call_args = mock_openai.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args.args[0].get("messages", [])
        # Find user message content
        user_content = None
        for m in call_args.kwargs["messages"]:
            if m["role"] == "user":
                user_content = m["content"]
        assert isinstance(user_content, list)
        has_image = any(item.get("type") == "image_url" for item in user_content)
        assert has_image

    def test_chat_raises_on_api_error(self):
        mock_openai = MagicMock()
        mock_openai.chat.completions.create.side_effect = Exception("API quota exceeded")

        client = LLMClient(provider="openai", api_key="sk-test")
        client._client = mock_openai

        with pytest.raises(LLMClientError, match="OpenAI API error"):
            client.chat(system_prompt="sys", user_text="hello")
