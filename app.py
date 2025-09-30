"""
HK LLM Travel Planner - Pure LLM Approach
A conversational AI travel planner for Hong Kong using only LLM intelligence.
"""

import streamlit as st
import openai
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Configuration
AKASH_API_KEY = "sk-UVKYLhiNf0MKXRqbnDiehA"
AKASH_BASE_URL = "https://chatapi.akash.network/api/v1"
MODEL_NAME = "DeepSeek-R1-Distill-Llama-70B"

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime

class LLMTravelPlanner:
    """Pure LLM-based travel planner for Hong Kong."""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=AKASH_API_KEY,
            base_url=AKASH_BASE_URL
        )
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get the comprehensive system prompt for Hong Kong travel planning."""
        return """You are an expert Hong Kong travel planner specializing in accessible tourism for families and seniors.

EXPERTISE:
- Complete knowledge of Hong Kong attractions, restaurants, transportation
- Accessibility features: wheelchair access, elevators, step-free routes
- Dietary accommodations: soft meals, vegetarian, halal, allergies
- Budget planning with senior/child discounts
- Safe, comfortable itineraries with appropriate pacing
- Weather considerations and seasonal recommendations
- Transportation: MTR, buses, taxis, ferries with accessibility info

GUIDELINES:
1. Always prioritize accessibility and safety
2. Limit to 2-3 venues per day to prevent fatigue
3. Include detailed accessibility information for each recommendation
4. Provide cost estimates with available discounts
5. Explain reasoning for each recommendation
6. Consider weather and walking distances
7. Ask clarifying questions when needed
8. Be conversational and helpful

RESPONSE FORMAT:
- For general questions: Provide helpful, detailed answers
- For itinerary requests: Create day-by-day plans with:
  * Venue names and descriptions
  * Accessibility features (elevators, wheelchair access, toilets)
  * Transportation instructions
  * Cost estimates
  * Timing recommendations
  * Why each venue is suitable for the user's needs

HONG KONG KNOWLEDGE BASE:
Key accessible attractions: Victoria Peak (Sky Terrace), Star Ferry, Hong Kong Museum of History, Science Museum, Hong Kong Park, Kowloon Park, Temple Street Night Market, Ladies' Market, Tsim Sha Tsui Promenade, Avenue of Stars, Hong Kong Space Museum, Cultural Centre.

Accessible restaurants: Dim sum at accessible hotels, soft meal options at major shopping malls, vegetarian restaurants in Central and Causeway Bay.

Transportation: MTR has elevator access at most stations, buses have wheelchair spaces, taxis are accessible, Star Ferry has assistance available.

Always provide specific, actionable advice based on the user's stated needs."""

    def get_response(self, user_message: str, conversation_history: List[ChatMessage]) -> str:
        """Get LLM response for user message."""
        try:
            # Prepare messages
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history (last 10 messages to manage context)
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Add current user message
            messages.append({
                "role": "user", 
                "content": user_message
            })
            
            # Get LLM response
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
                timeout=30
            )
            
            return response.choices[0].message.content
            
        except openai.APITimeoutError:
            return "⏰ The request timed out. Please try again with a shorter message."
        except openai.RateLimitError:
            return "🚦 I'm currently handling many requests. Please wait a moment and try again."
        except openai.APIError as e:
            return f"🔧 I encountered an API error: {str(e)}. Please try again."
        except Exception as e:
            return f"❌ An unexpected error occurred: {str(e)}. Please try again."

def initialize_session():
    """Initialize Streamlit session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            ChatMessage(
                role="assistant",
                content="🏙️ **Welcome to HK LLM Travel Planner!**\n\nI'm your AI travel assistant specialized in creating accessible Hong Kong itineraries for families and seniors.\n\n**Tell me about your travel plans:**\n- Who's traveling with you?\n- Any accessibility needs (wheelchair, mobility aids)?\n- Dietary preferences or restrictions?\n- Budget range per person/day?\n- How many days will you be visiting?\n- Any specific interests or must-see places?\n\nI'll create a personalized, accessible itinerary just for you! 🌟",
                timestamp=datetime.now()
            )
        ]
    
    if "planner" not in st.session_state:
        st.session_state.planner = LLMTravelPlanner()

def display_message(message: ChatMessage):
    """Display a chat message."""
    with st.chat_message(message.role):
        st.markdown(message.content)

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="HK LLM Travel Planner",
        page_icon="🏙️",
        layout="wide"
    )
    
    # Initialize session FIRST
    initialize_session()
    
    # Header
    st.title("🏙️ HK LLM Travel Planner")
    st.markdown("*Pure LLM-powered accessible travel planning for Hong Kong*")
    
    # Sidebar
    with st.sidebar:
        st.header("🤖 AI Assistant")
        st.success("✅ DeepSeek-R1 Connected")
        st.info(f"Model: {MODEL_NAME}")
        
        st.divider()
        
        st.header("🎯 Quick Examples")
        st.markdown("""
        **Try asking:**
        - "Plan a 3-day trip for elderly parents with wheelchairs"
        - "Vegetarian restaurants in Central with soft meals"
        - "Accessible attractions for families with young children"
        - "Budget-friendly itinerary under $100/day"
        """)
        
        st.divider()
        
        if st.button("🔄 New Conversation"):
            st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
            st.rerun()
        
        st.header("📊 Session Info")
        st.write(f"Messages: {len(st.session_state.messages)}")
    
    # Display conversation
    for message in st.session_state.messages:
        display_message(message)
    
    # Chat input
    if prompt := st.chat_input("Describe your Hong Kong travel plans..."):
        # Add user message
        user_message = ChatMessage(
            role="user",
            content=prompt,
            timestamp=datetime.now()
        )
        st.session_state.messages.append(user_message)
        
        # Display user message
        display_message(user_message)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Planning your perfect Hong Kong experience..."):
                response_content = st.session_state.planner.get_response(
                    prompt, 
                    st.session_state.messages[:-1]  # Exclude the just-added user message
                )
                
                st.markdown(response_content)
                
                # Add assistant message
                assistant_message = ChatMessage(
                    role="assistant",
                    content=response_content,
                    timestamp=datetime.now()
                )
                st.session_state.messages.append(assistant_message)

if __name__ == "__main__":
    main()