import re
import logging
from typing import Dict, Any, Optional, Tuple, List

logger = logging.getLogger(__name__)

class InputAnalyzer:
    """Fast rule-based input analysis for response rate optimization"""
    
    def __init__(self):
        # No API client needed - pure rule-based analysis
        pass
    
    def analyze_input_quality(self, conversation_input: str) -> Optional[Dict[str, Any]]:
        """Analyze input using fast rule-based heuristics"""
        
        if len(conversation_input.strip()) < 10:
            return None
        
        # Get score and suggestions using regex/keyword analysis
        score, suggestions = self._analyze_with_rules(conversation_input)
        
        # Convert to expected format with qualitative feedback
        return {
            "overall_score": self._get_response_likelihood(score),
            "suggestions": self._format_qualitative_suggestions(score, suggestions)
        }
    
    def _analyze_with_rules(self, text: str) -> Tuple[int, List[str]]:
        """Pure rule-based analysis - instant feedback"""
        score = 0
        suggestions = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Person identification (20 points)
        if re.search(r'met \w+ \w+', text_lower) or re.search(r'spoke with \w+', text_lower):
            score += 20
        else:
            suggestions.append("Include person's full name: 'Met [First Last]'")
        
        # Company context (15 points)  
        if any(word in text_lower for word in ['company', 'works at', 'from', 'at', 'vp', 'director', 'manager']):
            score += 15
        else:
            suggestions.append("Add where they work or their title")
            
        # Conversation depth (25 points)
        conversation_words = ['discussed', 'talked', 'mentioned', 'shared', 'explained', 'told me']
        conversation_count = sum(1 for word in conversation_words if word in text_lower)
        if conversation_count >= 2:
            score += 25
        elif conversation_count >= 1:
            score += 15
            suggestions.append("Add more conversation topics you discussed")
        else:
            suggestions.append("Add more conversation topics you discussed")
        
        # Personal connections (20 points)
        connection_words = ['alumni', 'school', 'university', 'both', 'shared', 'connection', 'same', 'also']
        if any(word in text_lower for word in connection_words):
            score += 20
        else:
            suggestions.append("Include any personal connections or shared background")
        
        # Follow-up opportunities (10 points)
        follow_up_words = ['introduce', 'refer', 'next step', 'follow up', 'contact', 'connect', 'send']
        if any(word in text_lower for word in follow_up_words):
            score += 10
        else:
            suggestions.append("Mention any follow-up opportunities they offered")
        
        # Detail level (10 points)
        if word_count >= 100:
            score += 10
        elif word_count >= 50:
            score += 5
            suggestions.append("Add more details for better personalization")
        else:
            suggestions.append("Provide more conversation details (aim for 100+ words)")
        
        return min(score, 100), suggestions
    
    def _get_response_likelihood(self, score: int) -> str:
        """Convert numerical score to qualitative likelihood"""
        if score >= 80:
            return "Extremely Likely"
        elif score >= 60:
            return "Likely" 
        elif score >= 40:
            return "Neutral"
        elif score >= 20:
            return "Unlikely"
        else:
            return "Extremely Unlikely"
    
    def _get_quality_level(self, category: str, has_issue: bool) -> str:
        """Convert to qualitative quality level"""
        if has_issue:
            if category == "person_identification":
                return "Missing"
            elif category == "conversation_topics":
                return "Needs Work"
            elif category == "personal_connections":
                return "Missing"
            elif category == "follow_up_opportunities":
                return "Needs Work"
            else:
                return "Needs Work"
        else:
            return "Excellent"
    
    def _format_qualitative_suggestions(self, score: int, suggestions: List[str]) -> Dict[str, Dict[str, str]]:
        """Format suggestions with qualitative feedback"""
        
        # Categorize suggestions
        person_suggestions = [s for s in suggestions if 'name' in s.lower() or 'title' in s.lower()]
        topic_suggestions = [s for s in suggestions if 'conversation' in s.lower() or 'discussed' in s.lower()]
        connection_suggestions = [s for s in suggestions if 'personal' in s.lower() or 'shared' in s.lower()]
        follow_up_suggestions = [s for s in suggestions if 'follow' in s.lower() or 'opportunities' in s.lower()]
        detail_suggestions = [s for s in suggestions if 'detail' in s.lower() or 'words' in s.lower()]
        
        formatted = {}
        
        # Person identification
        has_person_issue = len(person_suggestions) > 0
        formatted["person_identification"] = {
            "score": self._get_quality_level("person_identification", has_person_issue),
            "text": f"Person identification: **{self._get_quality_level('person_identification', has_person_issue)}**",
            "improvement": person_suggestions[0] if person_suggestions else "Great job including their name and title!"
        }
        
        # Conversation topics
        has_topic_issue = len(topic_suggestions) > 0
        formatted["conversation_topics"] = {
            "score": self._get_quality_level("conversation_topics", has_topic_issue),
            "text": f"Conversation topics: **{self._get_quality_level('conversation_topics', has_topic_issue)}**",
            "improvement": topic_suggestions[0] if topic_suggestions else "Excellent conversation depth!"
        }
        
        # Personal connections
        has_connection_issue = len(connection_suggestions) > 0
        formatted["personal_connections"] = {
            "score": self._get_quality_level("personal_connections", has_connection_issue),
            "text": f"Personal connections: **{self._get_quality_level('personal_connections', has_connection_issue)}**",
            "improvement": connection_suggestions[0] if connection_suggestions else "Great personal connection details!"
        }
        
        # Follow-up opportunities
        has_followup_issue = len(follow_up_suggestions) > 0
        formatted["follow_up_opportunities"] = {
            "score": self._get_quality_level("follow_up_opportunities", has_followup_issue),
            "text": f"Follow-up clarity: **{self._get_quality_level('follow_up_opportunities', has_followup_issue)}**",
            "improvement": follow_up_suggestions[0] if follow_up_suggestions else "Perfect follow-up opportunities mentioned!"
        }
        
        # Detail level
        has_detail_issue = len(detail_suggestions) > 0
        formatted["conversation_context"] = {
            "score": self._get_quality_level("conversation_context", has_detail_issue),
            "text": f"Context detail: **{self._get_quality_level('conversation_context', has_detail_issue)}**",
            "improvement": detail_suggestions[0] if detail_suggestions else "Great level of detail provided!"
        }
        
        return formatted
