# HK LLM Travel Planner 🏙️

A pure LLM-powered conversational travel planner for Hong Kong, designed specifically for accessible tourism for families and seniors.

## ✨ Features

- **Pure LLM Intelligence**: Uses DeepSeek-R1-Distill-Llama-70B via Akash Network
- **Conversational Interface**: Natural language interaction for travel planning
- **Accessibility-First**: Specialized in mobility, dietary, and safety needs
- **Real-time Planning**: Instant itinerary generation through AI reasoning
- **Zero Database**: All knowledge embedded in the LLM system prompt

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Streamlit
- OpenAI Python client

### Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 💬 How to Use

Simply start a conversation with the AI assistant:

**Example conversations:**
- "I'm planning a 3-day Hong Kong trip for my elderly parents who use wheelchairs and prefer soft meals. Budget is around $150 per day."
- "What are the most accessible attractions in Hong Kong for families with young children?"
- "Can you suggest vegetarian restaurants in Central that accommodate dietary restrictions?"

The AI will:
- Ask clarifying questions if needed
- Generate detailed day-by-day itineraries
- Provide accessibility information for each venue
- Include cost estimates and transportation details
- Explain reasoning for each recommendation

## 🏗️ Architecture

### Pure LLM Approach
- **Single File**: Everything in `app.py` - no complex architecture
- **LLM-Only Knowledge**: All Hong Kong travel information embedded in system prompt
- **Conversational State**: Simple message history management
- **Direct API Integration**: Straight connection to Akash Network

### Key Components
- `LLMTravelPlanner`: Core AI interaction class
- `ChatMessage`: Simple message data structure
- Streamlit chat interface with session management
- Comprehensive system prompt with Hong Kong expertise

## ⚙️ Configuration

The app uses Akash Network for LLM services:
- **API Endpoint**: `https://chatapi.akash.network/api/v1`
- **Model**: `DeepSeek-R1-Distill-Llama-70B`
- **API Key**: Configured in `app.py`

## 🎯 Design Philosophy

### Simplicity First
- Single file application
- No external databases or APIs
- Pure LLM reasoning for all recommendations
- Minimal dependencies

### LLM-Centric Intelligence
- All Hong Kong knowledge in system prompt
- AI reasoning for accessibility assessments
- Dynamic itinerary generation
- Contextual conversation management

### Accessibility Focus
- Wheelchair accessibility information
- Elevator and step-free access details
- Dietary accommodation guidance
- Senior-friendly pacing recommendations
- Budget-conscious planning with discounts

## 🌟 What Makes This Different

Unlike traditional travel apps that rely on databases and APIs, this planner uses pure LLM intelligence:

- **No Database**: All venue knowledge embedded in AI
- **Dynamic Reasoning**: AI evaluates accessibility on-the-fly
- **Conversational**: Natural language interaction throughout
- **Contextual**: Remembers conversation history for better recommendations
- **Explanatory**: AI explains why each recommendation is suitable

## 🔧 Customization

To adapt for other cities or use cases:

1. **Update System Prompt**: Modify the knowledge base in `_get_system_prompt()`
2. **Change Model**: Update `MODEL_NAME` for different LLM capabilities
3. **Adjust Parameters**: Modify `max_tokens`, `temperature` for different response styles

## 📝 Example System Prompt Structure

The AI is trained with comprehensive Hong Kong knowledge including:
- Accessible attractions and their features
- Restaurant options with dietary accommodations
- Transportation accessibility (MTR, buses, taxis)
- Cost estimates and discount information
- Weather and seasonal considerations

## 🤝 Contributing

This is a minimal, single-file application designed for simplicity. To contribute:
1. Test the conversation flows
2. Suggest improvements to the system prompt
3. Report any accessibility gaps in recommendations

## 📄 License

Open source - feel free to adapt for other cities or travel needs!

---

**Built with pure LLM intelligence for accessible Hong Kong travel** 🌟