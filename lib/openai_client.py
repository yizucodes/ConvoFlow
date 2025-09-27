"""OpenAI client wrapper for GPT-based conversation analysis and email generation."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Optional

import openai
import streamlit as st


logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client encapsulating OpenAI chat completion functionality."""

    def __init__(self, *, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found")

        openai.api_key = self.api_key
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")

    def analyze_conversation(self, conversation_text: str, system_prompt: str) -> Optional[Dict[str, Any]]:
        """Analyze a conversation and return structured JSON data."""

        request_options = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation_text},
            ],
            "response_format": {"type": "json_object"},
        }

        try:
            response = openai.chat.completions.create(**request_options)

            return json.loads(response.choices[0].message.content)

        except json.JSONDecodeError as exc:
            logger.error("Failed to parse GPT response as JSON", exc_info=exc)
            st.error("Failed to parse GPT response as JSON")
            return None
        except Exception as exc:  # pragma: no cover - network failure path
            logger.exception("OpenAI API error during conversation analysis")
            st.error(f"OpenAI API error: {exc}")
            return None

    def generate_email(self, email_request: str, system_prompt: str) -> Optional[str]:
        """Generate a follow-up email using GPT."""

        request_options = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_request},
            ],
        }

        try:
            response = openai.chat.completions.create(**request_options)

            return response.choices[0].message.content.strip()

        except Exception as exc:  # pragma: no cover - network failure path
            logger.exception("OpenAI API error during email generation")
            st.error(f"Email generation error: {exc}")
            return None

