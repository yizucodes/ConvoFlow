"""Unit tests for utils package."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.prompts import CONVERSATION_ANALYSIS_PROMPT, EMAIL_GENERATION_PROMPT
from utils.validation import ConversationValidator


def test_prompts_loaded():
    """Test that prompts are properly loaded."""
    assert CONVERSATION_ANALYSIS_PROMPT is not None
    assert len(CONVERSATION_ANALYSIS_PROMPT) > 100
    assert "JSON" in CONVERSATION_ANALYSIS_PROMPT
    
    assert EMAIL_GENERATION_PROMPT is not None
    assert len(EMAIL_GENERATION_PROMPT) > 100
    assert "email" in EMAIL_GENERATION_PROMPT.lower()


def test_validation_valid_input():
    """Test validation with valid conversation input."""
    valid_text = "Met Sarah Chen at the AI meetup. We discussed machine learning infrastructure and she mentioned struggling with hiring ML engineers. She works at Databricks and seemed really interested in our conversation about scaling models."
    
    is_valid, errors = ConversationValidator.validate_conversation_input(valid_text)
    assert is_valid
    assert len(errors) == 0


def test_validation_empty_input():
    """Test validation with empty input."""
    is_valid, errors = ConversationValidator.validate_conversation_input("")
    assert not is_valid
    assert "Conversation description is required" in errors


def test_validation_too_short():
    """Test validation with too short input."""
    is_valid, errors = ConversationValidator.validate_conversation_input("Met someone.")
    assert not is_valid
    assert any("minimum 50 characters" in error for error in errors)


def test_validation_no_conversation_indicators():
    """Test validation without conversation indicators."""
    is_valid, errors = ConversationValidator.validate_conversation_input("This is just some random text without any conversation context.")
    assert not is_valid
    # Should have either conversation or person identification error
    assert any("describe an actual conversation" in error or "include the person's name" in error for error in errors)


def test_validation_no_person_identification():
    """Test validation without person identification."""
    is_valid, errors = ConversationValidator.validate_conversation_input("We discussed AI tools and machine learning at the conference.")
    assert not is_valid
    assert any("include the person's name" in error for error in errors)


def test_get_suggestions():
    """Test input improvement suggestions."""
    text = "Met someone at event."
    suggestions = ConversationValidator.get_input_suggestions(text)
    assert len(suggestions) > 0
    assert any("where the person works" in suggestion.lower() for suggestion in suggestions)
