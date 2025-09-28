import pytest
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from lib.input_analyzer import InputAnalyzer

# Load environment variables
load_dotenv()

def test_analyze_input_quality_good_input():
    """Test analysis with good input"""
    analyzer = InputAnalyzer()
    
    # Test good input
    good_input = "Met Sarah Chen, VP of Engineering at Databricks at the NYC AI meetup. We discussed their OpenAI partnership and ML hiring challenges. We're both UW alumni and bonded over work-life balance concerns. She offered to introduce me to their recruiting team."
    
    result = analyzer.analyze_input_quality(good_input)
    
    print("\n=== INPUT ANALYSIS TEST OUTPUT ===")
    print(f"Input: {good_input}")
    print(f"Analysis result: {result}")
    print("=" * 40)
    
    assert result is not None
    assert isinstance(result, dict)
    assert 'overall_score' in result
    assert 'suggestions' in result
    # Test qualitative feedback - good input should be "Likely" or "Extremely Likely"
    assert result['overall_score'] in ["Likely", "Extremely Likely"]
    assert len(result['suggestions']) == 5

def test_analyze_input_quality_poor_input():
    """Test analysis with poor input"""
    analyzer = InputAnalyzer()
    
    # Test poor input
    poor_input = "met someone at conference"
    
    result = analyzer.analyze_input_quality(poor_input)
    
    print("\n=== POOR INPUT ANALYSIS TEST OUTPUT ===")
    print(f"Input: {poor_input}")
    print(f"Analysis result: {result}")
    print("=" * 40)
    
    assert result is not None
    assert isinstance(result, dict)
    assert 'overall_score' in result
    assert 'suggestions' in result
    # Test qualitative feedback - poor input should be "Unlikely" or "Extremely Unlikely"
    assert result['overall_score'] in ["Unlikely", "Extremely Unlikely", "Neutral"]

def test_analyze_input_quality_short_input():
    """Test analysis with short input (should return None)"""
    analyzer = InputAnalyzer()
    
    # Test short input
    short_input = "met someone"
    
    result = analyzer.analyze_input_quality(short_input)
    
    assert result is None

def test_analyze_input_quality_empty_input():
    """Test analysis with empty input (should return None)"""
    analyzer = InputAnalyzer()
    
    # Test empty input
    empty_input = ""
    
    result = analyzer.analyze_input_quality(empty_input)
    
    assert result is None
