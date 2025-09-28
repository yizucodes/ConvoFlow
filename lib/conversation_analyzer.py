from typing import Dict, Any, Optional
from .openai_client import OpenAIClient
from utils.prompts import CONVERSATION_ANALYSIS_PROMPT

class ConversationAnalyzer:
    def __init__(self):
        self.client = OpenAIClient()
    
    def analyze(self, conversation_text: str) -> Optional[Dict[str, Any]]:
        """Analyze conversation and return structured insights"""
        if not self._validate_input(conversation_text):
            return None
        
        analysis = self.client.analyze_conversation(
            conversation_text=conversation_text,
            system_prompt=CONVERSATION_ANALYSIS_PROMPT
        )
        
        if analysis:
            # Post-process analysis to ensure data quality
            analysis = self._clean_analysis_data(analysis)
        
        return analysis
    
    def _validate_input(self, text: str) -> bool:
        """Validate conversation input"""
        if not text or len(text.strip()) < 50:
            return False
        
        # Check for minimum conversation elements
        required_elements = ["met", "discussed", "conversation"]
        if not any(element in text.lower() for element in required_elements):
            return False
        
        return True
    
    def _clean_analysis_data(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate analysis data"""
        # Ensure all required keys exist with defaults
        defaults = {
            "person": {"name": "Unknown", "title": "Unknown", "company": "Unknown"},
            "conversation_context": {
                "topics_discussed": [],
                "personal_connections": [],
                "conversation_quality": "brief"
            },
            "relationship_signals": {
                "receptiveness_score": "Moderate interaction with professional communication style",
                "communication_style": "professional",
                "follow_up_readiness": "within_week"
            }
        }
        
        # Merge defaults with analysis
        for key, default_value in defaults.items():
            if key not in analysis:
                analysis[key] = default_value
            elif isinstance(default_value, dict):
                for subkey, subdefault in default_value.items():
                    if subkey not in analysis[key]:
                        analysis[key][subkey] = subdefault
        
        return analysis
