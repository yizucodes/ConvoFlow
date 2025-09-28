# ConvoFlow - AI Networking Assistant

Transform networking conversations into relationship-building follow-up emails using AI-powered conversation analysis and personalized email generation.

## 🚀 Features

- **Real-time Input Analysis**: Instant feedback on conversation quality with qualitative scoring
- **GPT-5 Conversation Intelligence**: Deep analysis of relationship signals and communication style
- **Personalized Email Generation**: AI-generated follow-up emails that reference specific conversation details
- **Rule-based Input Optimization**: Fast, offline analysis for immediate feedback
- **Professional UI**: Clean, intuitive interface with side-by-side input and analysis

## 🏗️ Architecture

```
convoflow/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── lib/
│   ├── conversation_analyzer.py  # GPT-5 conversation analysis
│   ├── email_generator.py      # AI email generation
│   ├── input_analyzer.py       # Rule-based input optimization
│   └── openai_client.py        # OpenAI API integration
├── utils/
│   ├── prompts.py             # Validated GPT prompts
│   └── validation.py          # Input validation utilities
└── tests/                     # Unit and integration tests
```

## 🚀 Data Flow
<img width="510" height="364" alt="image" src="https://github.com/user-attachments/assets/406f8a0d-1622-42fe-af6b-60a5e85ecbf3" />

## 🛠️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

Visit `http://localhost:8501` to use the app.

## 💡 How It Works

1. **Describe Your Conversation**: Enter details about your networking interaction
2. **Get Real-time Feedback**: AI Input Assistant provides instant qualitative feedback
3. **Analyze with GPT-5**: Deep conversation analysis extracts relationship signals
4. **Generate Personalized Email**: AI creates a follow-up email using conversation context
5. **Copy and Send**: Professional, personalized email ready to send

## 🎯 Key Features

### Real-time Input Analysis
- **Instant feedback** on conversation quality
- **Qualitative scoring**: "Extremely Likely", "Likely", "Neutral", etc.
- **Actionable suggestions** for improvement
- **Rule-based analysis** for speed and reliability

### GPT-5 Conversation Intelligence
- **Relationship signal analysis** (receptiveness, communication style)
- **Personal connection identification** (shared background, interests)
- **Follow-up strategy recommendations** (tone, timing, objectives)
- **Confidence scoring** for analysis quality

### AI Email Generation
- **Context-aware personalization** using conversation details
- **Professional tone matching** based on recipient's communication style
- **Natural formatting** without AI-generated artifacts
- **Compelling subject lines** that reference conversation elements

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Tests cover:
- Unit tests for input analysis
- Integration tests for OpenAI API
- UI component testing
- Business logic validation

## 📊 Performance

- **Input Analysis**: Instant (rule-based)
- **Conversation Analysis**: 5-10 seconds (GPT-5 API)
- **Email Generation**: 3-5 seconds (GPT-5 API)
- **Caching**: LRU cache for repeated inputs

## 🔧 Configuration

### Streamlit Settings (`.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
headless = true
port = 8501
```

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Add `OPENAI_API_KEY` in secrets
4. Deploy

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_api_key"

# Run the app
streamlit run app.py
```

## 📝 Example Usage

**Input:**
```
Met Sarah Chen, VP of Engineering at Databricks, at the NYC AI Founders meetup. She seemed really excited when talking about their OpenAI partnership but mentioned struggling to find ML engineers with both technical depth and product sense. We bonded over both being UW alumni and shared concerns about work-life balance in tech. She suggested I should check out their new grad program and offered to make an introduction to their recruiting team.
```

**AI Analysis:**
- Response Likelihood: **Extremely Likely** 🚀
- Personal Connections: UW alumni, shared work-life balance concerns
- Communication Style: Professional yet enthusiastic
- Follow-up Readiness: Within week

**Generated Email:**
- References specific conversation topics (OpenAI partnership, ML engineering challenges)
- Leverages personal connections (UW alumni)
- Matches professional yet enthusiastic tone
- Includes clear next steps (new grad program, recruiting team introduction)

---

**Built with ❤️ using Streamlit and OpenAI GPT-5**
