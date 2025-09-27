import re
from typing import Tuple, List

class ConversationValidator:
    
    @staticmethod
    def validate_conversation_input(text: str) -> Tuple[bool, List[str]]:
        """Validate conversation input and return validation status with error messages"""
        errors = []
        
        if not text or not text.strip():
            errors.append("Conversation description is required")
            return False, errors
        
        text = text.strip()
        
        # Minimum length check
        if len(text) < 50:
            errors.append("Please provide more details about your conversation (minimum 50 characters)")
        
        # Maximum length check
        if len(text) > 2000:
            errors.append("Conversation description is too long (maximum 2000 characters)")
        
        # Check for basic conversation elements
        conversation_indicators = [
            r'\bmet\b', r'\bdiscussed\b', r'\btalked\b', r'\bconversation\b', 
            r'\bspoke\b', r'\bchatted\b', r'\bmentioned\b'
        ]
        
        if not any(re.search(pattern, text, re.IGNORECASE) for pattern in conversation_indicators):
            errors.append("Please describe an actual conversation (mention what you discussed or talked about)")
        
        # Check for person identification
        person_indicators = [
            r'\bmet [A-Z][a-z]+', r'\bspoke with [A-Z][a-z]+', 
            r'\bchatted with [A-Z][a-z]+', r'[A-Z][a-z]+ from',
            r'[A-Z][a-z]+ [A-Z][a-z]+', r'[A-Z][a-z]+ at'
        ]
        
        if not any(re.search(pattern, text) for pattern in person_indicators):
            errors.append("Please include the person's name or how you can identify them")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @staticmethod
    def get_input_suggestions(text: str) -> List[str]:
        """Provide suggestions to improve input quality"""
        suggestions = []
        
        if text and len(text.strip()) > 0:
            text_lower = text.lower()
            
            # Suggest adding company info
            if "company" not in text_lower and "works at" not in text_lower:
                suggestions.append("Consider mentioning where the person works")
            
            # Suggest adding conversation details
            if "discussed" not in text_lower and "talked about" not in text_lower:
                suggestions.append("Add more details about what you specifically discussed")
            
            # Suggest adding relationship context
            if "background" not in text_lower and "connection" not in text_lower:
                suggestions.append("Mention any shared background or connections you discovered")
        
        return suggestions
