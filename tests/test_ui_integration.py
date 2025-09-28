import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

def test_display_ai_assistant_short_input():
    """Test that AI assistant doesn't show for short input"""
    from app import display_ai_assistant
    
    # Mock streamlit components
    with patch('streamlit.expander') as mock_expander:
        display_ai_assistant("short")
        
        # Should not call expander for short input
        mock_expander.assert_not_called()

def test_display_ai_assistant_long_input():
    """Test that AI assistant shows for long input"""
    from app import display_ai_assistant
    
    # Mock the analyzer and streamlit components
    mock_analysis = {
        'overall_score': 7.5,
        'suggestions': {
            'person_identification': {
                'score': 8,
                'text': 'Person identification: Excellent!',
                'improvement': 'Add their name and title - increases response rate by 30%'
            }
        }
    }
    
    with patch('lib.input_analyzer.InputAnalyzer') as mock_analyzer_class:
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_input_quality.return_value = mock_analysis
        mock_analyzer_class.return_value = mock_analyzer
        
        with patch('streamlit.expander') as mock_expander:
            mock_expander_context = MagicMock()
            mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
            mock_expander.return_value.__exit__ = MagicMock(return_value=None)
            
            display_ai_assistant("This is a longer input that should trigger the AI assistant")
            
            # Should call expander for long input
            mock_expander.assert_called_once_with("🧠 AI Input Assistant", expanded=True)

def test_display_ai_assistant_no_analysis():
    """Test that AI assistant handles no analysis gracefully"""
    from app import display_ai_assistant
    
    # Mock the cached analyzer function to return None
    with patch('app.analyze_input_with_cache', return_value=None):
        with patch('streamlit.expander') as mock_expander:
            display_ai_assistant("This is a longer input that should trigger the AI assistant")
            
            # Should not call expander if no analysis
            mock_expander.assert_not_called()

if __name__ == "__main__":
    pytest.main([__file__])
