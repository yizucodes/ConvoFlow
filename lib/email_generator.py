from typing import Optional
from .openai_client import OpenAIClient
from utils.prompts import EMAIL_GENERATION_PROMPT

class EmailGenerator:
    def __init__(self):
        self.client = OpenAIClient()
    
    def generate_follow_up(self, analysis_data: dict, additional_context: str = "") -> Optional[str]:
        """Generate follow-up email based on conversation analysis"""
        
        # Build the email generation request
        email_request = self._build_email_request(analysis_data, additional_context)
        
        # Generate email
        email = self.client.generate_email(
            email_request=email_request,
            system_prompt=EMAIL_GENERATION_PROMPT
        )
        
        if email:
            email = self._clean_email_output(email)
        
        return email
    
    def _build_email_request(self, analysis: dict, additional_context: str) -> str:
        """Build structured email generation request"""
        person = analysis.get("person", {})
        context = analysis.get("conversation_context", {})
        strategy = analysis.get("follow_up_strategy", {})
        
        request = f"""
Generate a follow-up email based on this conversation analysis:

PERSON: {person.get('name', 'Unknown')}, {person.get('title', 'Professional')} at {person.get('company', 'Company')}

ACTUAL CONVERSATION DETAILS:
"""
        
        # Add conversation details
        if context.get("topics_discussed"):
            request += f"- Topics discussed: {', '.join(context['topics_discussed'])}\n"
        
        if context.get("personal_connections"):
            request += f"- Personal connections: {', '.join(context['personal_connections'])}\n"
        
        if context.get("opportunities_expressed"):
            request += f"- Opportunities mentioned: {', '.join(context['opportunities_expressed'])}\n"
        
        # Add follow-up strategy
        if strategy.get("primary_objective"):
            request += f"\nFOLLOW-UP OBJECTIVE: {strategy['primary_objective']}\n"
        
        if strategy.get("recommended_tone"):
            request += f"TONE: {strategy['recommended_tone']}\n"
        
        # Add additional context if provided
        if additional_context:
            request += f"\nADDITIONAL CONTEXT: {additional_context}\n"
        
        request += "\nWrite email with subject line that references only confirmed conversation elements."
        
        return request
    
    def _clean_email_output(self, email: str) -> str:
        """Clean and format email output"""
        # Remove any GPT artifacts
        email = email.replace("Subject:", "**Subject:**", 1)
        
        # Ensure proper formatting
        lines = email.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        return '\n\n'.join(cleaned_lines)
