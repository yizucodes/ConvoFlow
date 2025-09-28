"""Integration tests for OpenAIClient that require real OpenAI API access."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from lib.openai_client import OpenAIClient


load_dotenv()


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set",
)
def test_generate_email_live_call() -> None:
    """Ensure live email generation call returns a non-empty response."""

    client = OpenAIClient()
    email = client.generate_email(
        email_request="Generate a short friendly email acknowledging our recent chat about AI tools.",
        system_prompt="You are a helpful email assistant.",
    )

    print("\n=== EMAIL GENERATION TEST OUTPUT ===")
    print(f"Generated email:\n{email}")
    print(f"Email length: {len(email) if email else 0}")
    print("=" * 40)

    assert email is not None
    assert len(email) > 0


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set",
)
def test_analyze_conversation_live_call() -> None:
    """Ensure live conversation analysis call returns structured JSON data."""

    client = OpenAIClient()
    analysis = client.analyze_conversation(
        conversation_text="We met at a meetup and discussed advances in AI infrastructure and hiring challenges.",
        system_prompt="You analyze conversations and return JSON.",
    )

    print("\n=== CONVERSATION ANALYSIS TEST OUTPUT ===")
    print(f"Analysis result:\n{analysis}")
    print(f"Analysis type: {type(analysis)}")
    print(f"Analysis keys: {list(analysis.keys()) if isinstance(analysis, dict) else 'N/A'}")
    print("=" * 45)

    assert analysis is not None
    assert isinstance(analysis, dict)
    assert analysis  # Non-empty result

