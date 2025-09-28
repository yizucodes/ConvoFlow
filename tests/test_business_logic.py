"""Integration tests for business logic layer."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from lib.conversation_analyzer import ConversationAnalyzer
from lib.email_generator import EmailGenerator

load_dotenv()


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set",
)
def test_conversation_analyzer_integration():
    """Test conversation analyzer with real API call."""
    analyzer = ConversationAnalyzer()
    
    conversation_text = """
    Met Sarah Chen, VP of Engineering at Databricks, at the NYC AI Founders meetup. 
    She seemed really excited when talking about their OpenAI partnership but mentioned 
    struggling to find ML engineers with both technical depth and product sense. 
    We bonded over both being UW alumni and shared concerns about work-life balance in tech. 
    She suggested I should check out their new grad program and offered to make an introduction 
    to their recruiting team. The conversation lasted about 20 minutes and felt very natural.
    """
    
    analysis = analyzer.analyze(conversation_text)
    
    print("\n=== CONVERSATION ANALYSIS INTEGRATION TEST ===")
    print(f"Analysis result: {analysis}")
    print("=" * 50)
    
    assert analysis is not None
    assert isinstance(analysis, dict)
    assert "person" in analysis
    assert "conversation_context" in analysis
    assert "relationship_signals" in analysis


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set",
)
def test_email_generator_integration():
    """Test email generator with real API call."""
    generator = EmailGenerator()
    
    # Mock analysis data
    analysis_data = {
        "person": {
            "name": "Sarah Chen",
            "title": "VP of Engineering",
            "company": "Databricks"
        },
        "conversation_context": {
            "topics_discussed": ["OpenAI partnership", "ML engineering hiring", "UW alumni connection"],
            "personal_connections": ["Both UW alumni", "Shared work-life balance concerns"],
            "opportunities_expressed": ["New grad program", "Recruiting team introduction"]
        },
        "follow_up_strategy": {
            "primary_objective": "Follow up on recruiting team introduction",
            "recommended_tone": "Professional but warm",
            "key_personalization_hooks": ["UW alumni connection", "OpenAI partnership discussion", "Work-life balance concerns"]
        }
    }
    
    email = generator.generate_follow_up(analysis_data, "Interested in ML engineering roles")
    
    print("\n=== EMAIL GENERATION INTEGRATION TEST ===")
    print(f"Generated email:\n{email}")
    print("=" * 50)
    
    assert email is not None
    assert len(email) > 0
    assert "Sarah" in email or "Databricks" in email


def test_conversation_analyzer_validation():
    """Test conversation analyzer input validation."""
    analyzer = ConversationAnalyzer()
    
    # Test with invalid input
    result = analyzer.analyze("")
    assert result is None
    
    result = analyzer.analyze("Short text")
    assert result is None
    
    # Note: The analyzer is lenient and will process text even without conversation indicators
    # This is by design - it will return analysis with low confidence scores
    result = analyzer.analyze("Just some random text without conversation context")
    # Should return analysis but with low confidence
    assert result is not None
    assert result.get("confidence_scores", {}).get("overall_analysis", "0") in ["1/10", "2/10", "3/10"]


def test_email_generator_request_building():
    """Test email generator request building logic."""
    generator = EmailGenerator()
    
    analysis_data = {
        "person": {"name": "John Doe", "title": "Engineer", "company": "TechCorp"},
        "conversation_context": {
            "topics_discussed": ["AI tools", "Machine learning"],
            "personal_connections": ["Both from Stanford"]
        },
        "follow_up_strategy": {
            "primary_objective": "Schedule follow-up call",
            "recommended_tone": "Professional"
        }
    }
    
    request = generator._build_email_request(analysis_data, "Additional context here")
    
    assert "John Doe" in request
    assert "TechCorp" in request
    assert "AI tools" in request
    assert "Stanford" in request
    assert "Additional context here" in request


def test_email_cleaning():
    """Test email output cleaning."""
    generator = EmailGenerator()
    
    dirty_email = "Subject: Test\n\nHi there,\n\nThis is a test.\n\nBest regards"
    cleaned = generator._clean_email_output(dirty_email)
    
    assert "**Subject:**" in cleaned
    assert cleaned.count("\n\n") >= 2  # Should have proper paragraph breaks
