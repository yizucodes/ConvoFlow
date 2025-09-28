import streamlit as st
import os
import time
from functools import lru_cache
from dotenv import load_dotenv
from lib.conversation_analyzer import ConversationAnalyzer
from lib.email_generator import EmailGenerator
# Removed old validation system - now using AI Input Assistant

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ConvoFlow - AI Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .conversation-input {
        border-radius: 10px;
        border: 2px solid #E8E8E8;
    }
    .analysis-container {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .email-container {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'conversation_analysis' not in st.session_state:
        st.session_state.conversation_analysis = None
    if 'generated_email' not in st.session_state:
        st.session_state.generated_email = None

def display_header():
    """Display application header"""
    st.markdown('<h1 style="text-align: left; margin-bottom: 20px; font-size: 1.8rem; color: #1f77b4;">ConvoFlow - AI Networking Assistant</h1>', unsafe_allow_html=True)

@lru_cache(maxsize=100)
def analyze_input_with_cache(conversation_input: str):
    """Cached input analysis to prevent excessive API calls"""
    from lib.input_analyzer import InputAnalyzer
    analyzer = InputAnalyzer()
    return analyzer.analyze_input_quality(conversation_input)

def display_ai_assistant(conversation_input: str):
    """Display real-time AI input guidance with qualitative feedback"""
    
    if len(conversation_input.strip()) < 10:
        return
    
    # Get instant analysis (no debouncing needed with rule-based approach)
    analysis = analyze_input_with_cache(conversation_input)
    
    if not analysis:
        return
    
    with st.expander("🧠 AI Input Assistant", expanded=True):
        # Show qualitative response likelihood with emoji
        likelihood = analysis['overall_score']
        likelihood_emoji = {
            "Extremely Likely": "🚀",
            "Likely": "📈", 
            "Neutral": "😐",
            "Unlikely": "📉",
            "Extremely Unlikely": "⚠️"
        }
        
        st.metric("Response Likelihood", f"{likelihood} {likelihood_emoji.get(likelihood, '📊')}")
        
        # Show specific suggestions with qualitative feedback
        has_issues = False
        for factor, suggestion in analysis['suggestions'].items():
            if suggestion['score'] in ['Missing', 'Needs Work']:
                st.warning(f"💡 {suggestion['improvement']}")
                has_issues = True
            else:
                st.success(f"✅ {suggestion['text']}")
        
        # Only show improvement message if there are actual issues
        if has_issues:
            st.info("💡 You can submit now, but improving these areas will increase response rates!")

def display_conversation_input():
    """Display conversation input section with AI guidance"""
    st.subheader("1. Describe Your Networking Conversation")
    
    placeholder_text = """Example:
Met Sarah Chen, VP of Engineering at Databricks, at the NYC AI Founders meetup. She seemed really excited when talking about their OpenAI partnership but mentioned struggling to find ML engineers with both technical depth and product sense. We bonded over both being UW alumni and shared concerns about work-life balance in tech. She suggested I should check out their new grad program and offered to make an introduction to their recruiting team. The conversation lasted about 20 minutes and felt very natural."""
    
    # Create two columns: left for input, right for AI assistant
    col1, col2 = st.columns([2, 1])  # 2:1 ratio for input:assistant
    
    with col1:
        conversation_input = st.text_area(
            "Describe your conversation with specific details about the person, their role, and what you discussed:",
            height=200,  # Increased height for better visibility
            placeholder=placeholder_text,
            help="Include: Person's name & title, their company, specific topics discussed, personal connections discovered, conversation tone, and any follow-up hints they gave"
        )
    
    with col2:
        # Show AI assistant for real-time guidance on the right side
        display_ai_assistant(conversation_input)
    
    # Button positioned directly under the input box (left column)
    with col1:
        # Button is disabled when no text or text is too short
        is_disabled = not conversation_input or len(conversation_input.strip()) < 20
        generate_button = st.button(
            "Generate Email", 
            type="primary", 
            disabled=is_disabled,
            help="Enter at least 20 characters to generate personalized email",
            use_container_width=True
        )
    
    return conversation_input, generate_button

# Removed old validation function - now using AI Input Assistant for real-time feedback

def generate_email(conversation_input):
    """Generate email and analysis in one step"""
    with st.spinner("Generating personalized email..."):
        # First analyze the conversation
        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze(conversation_input)
        
        if not analysis:
            st.error("Failed to analyze conversation. Please try again with more details.")
            return False
        
        # Store analysis
        st.session_state.conversation_analysis = analysis
        st.session_state.analysis_complete = True
        
        # Generate email
        generator = EmailGenerator()
        email = generator.generate_follow_up(analysis)
        
        if email:
            st.session_state.generated_email = email
            st.success("Email generated successfully!")
            return True
        else:
            st.error("Failed to generate email. Please try again.")
            return False

def display_analysis_results():
    """Display conversation analysis results in expandable section"""
    if not st.session_state.conversation_analysis:
        return
    
    analysis = st.session_state.conversation_analysis
    
    with st.expander("🧠 Conversation Intelligence", expanded=False):
        st.markdown("### Person Information")
        person = analysis.get('person', {})
        if person.get('name') != 'Unknown':
            st.markdown(f"**Name:** {person.get('name')} - {person.get('title')} at {person.get('company')}")
        
        # Key insights in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Key Relationship Signals:**")
            context = analysis.get('conversation_context', {})
            
            if context.get('personal_connections'):
                st.write("🤝 Personal Connections:")
                for connection in context['personal_connections']:
                    st.write(f"  • {connection}")
            
            if context.get('topics_discussed'):
                st.write("💬 Topics Discussed:")
                for topic in context['topics_discussed'][:3]:  # Show top 3
                    st.write(f"  • {topic}")
        
        with col2:
            st.markdown("**Communication Strategy:**")
            signals = analysis.get('relationship_signals', {})
            strategy = analysis.get('follow_up_strategy', {})
            
            if signals.get('receptiveness_score'):
                st.write(f"📊 Receptiveness: {signals['receptiveness_score']}")
            
            if strategy.get('recommended_tone'):
                st.write(f"🎯 Recommended Tone: {strategy['recommended_tone']}")
            
            if strategy.get('optimal_timing'):
                st.write(f"⏰ Optimal Timing: {strategy['optimal_timing']}")

def display_generated_email():
    """Display the generated email"""
    if not st.session_state.generated_email:
        return
    
    st.subheader("2. Generated Follow-up Email")
    
    # Display the email
    st.markdown('<div class="email-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.generated_email)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show personalization elements
    display_personalization_breakdown()

def display_personalization_breakdown():
    """Show what personalization elements were used"""
    if not st.session_state.conversation_analysis:
        return
    
    with st.expander("🎯 Personalization Elements Used"):
        analysis = st.session_state.conversation_analysis
        strategy = analysis.get('follow_up_strategy', {})
        
        if strategy.get('key_personalization_hooks'):
            st.write("**Key Personalization Hooks:**")
            for hook in strategy['key_personalization_hooks']:
                st.write(f"✓ {hook}")
        
        context = analysis.get('conversation_context', {})
        if context.get('personal_connections'):
            st.write("**Personal Connections Leveraged:**")
            for connection in context['personal_connections']:
                st.write(f"✓ {connection}")

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    
    # Input section
    conversation_input, generate_button = display_conversation_input()
    
    # Handle email generation when button is clicked
    if generate_button and conversation_input:
        if generate_email(conversation_input):
            st.rerun()
    
    # Display results if generation is complete
    if st.session_state.analysis_complete:
        display_generated_email()
        display_analysis_results()  # Now in expandable section
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("How to Use ConvoFlow")
        st.markdown("""
        1. **Describe your conversation** in detail
        2. **Generate personalized email** with one click
        3. **Explore conversation insights** (optional)
        4. **Select and copy** the email text above
        """)
        
        st.header("Tips for Best Results")
        st.markdown("""
        • Include specific conversation topics
        • Mention any personal connections
        • Note the person's role and company
        • Describe the conversation tone/quality
        • Include any follow-up hints they gave
        """)

if __name__ == "__main__":
    main()