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
MODEL_NAME = "DeepSeek-V3-1"

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
                content="🏙️ **Welcome to HK LLM Travel Planner!**\n\nI'm your AI travel assistant specialized in creating accessible Hong Kong itineraries for families and seniors.\n\n**Use the quick options below or describe your travel plans in detail!** 🌟",
                timestamp=datetime.now()
            )
        ]
    
    if "planner" not in st.session_state:
        st.session_state.planner = LLMTravelPlanner()

def create_quick_options():
    """Create quick option buttons for common travel scenarios."""
    st.markdown("### 🚀 Quick Planning Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👴👵 Senior-Friendly Trip", use_container_width=True):
            return "Plan a 3-day accessible Hong Kong trip for elderly travelers who need wheelchair access, prefer soft meals, and want to avoid too much walking. Budget around $150 per day."
        
        if st.button("👨‍👩‍👧‍👦 Family Adventure", use_container_width=True):
            return "Create a 4-day family-friendly Hong Kong itinerary for parents with young children (ages 5-12). Include kid-friendly attractions, accessible facilities, and budget around $120 per person per day."
    
    with col2:
        if st.button("🥗 Vegetarian Explorer", use_container_width=True):
            return "Recommend vegetarian and vegan restaurants in Hong Kong with accessible locations. Include soft meal options and dietary accommodation details."
        
        if st.button("💰 Budget Traveler", use_container_width=True):
            return "Plan a budget-friendly 2-day Hong Kong itinerary under $80 per day, focusing on free attractions, affordable food, and accessible public transportation."
    
    with col3:
        if st.button("🏛️ Culture & History", use_container_width=True):
            return "Design a cultural Hong Kong experience focusing on museums, temples, and historical sites with full accessibility information and transportation details."
        
        if st.button("🌃 First-Time Visitor", use_container_width=True):
            return "Create a must-see Hong Kong itinerary for first-time visitors, including iconic attractions like Victoria Peak, Star Ferry, and Temple Street Night Market with accessibility details."
    
    return None

def create_custom_form():
    """Create a detailed customizable form for specific travel requirements."""
    with st.expander("📋 **Detailed Planning Form** - Customize Your Perfect Trip", expanded=False):
        st.markdown("*Fill out this form for a highly personalized Hong Kong itinerary*")
        
        # Family Composition
        st.subheader("👥 Family Composition")
        col1, col2 = st.columns(2)
        
        with col1:
            adults = st.number_input("Number of Adults", min_value=1, max_value=10, value=2)
            seniors = st.number_input("Number of Seniors (65+)", min_value=0, max_value=10, value=0)
        
        with col2:
            children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
            if children > 0:
                child_ages = st.text_input("Children's Ages (e.g., 5, 8, 12)", placeholder="5, 8, 12")
        
        # Mobility Requirements
        st.subheader("♿ Mobility Requirements")
        mobility_needs = st.multiselect(
            "Select all that apply:",
            [
                "Wheelchair user",
                "Walking aid (cane, walker)",
                "Limited walking distance",
                "Need elevator access",
                "Avoid stairs completely",
                "Frequent rest breaks needed",
                "Mobility scooter user"
            ]
        )
        
        mobility_notes = st.text_area("Additional mobility considerations:", placeholder="Any specific mobility needs or concerns...")
        
        # Dietary Preferences
        st.subheader("🍽️ Dietary Preferences & Restrictions")
        dietary_prefs = st.multiselect(
            "Select all that apply:",
            [
                "Soft meals required",
                "Vegetarian",
                "Vegan",
                "Halal",
                "Kosher",
                "Gluten-free",
                "Dairy-free",
                "No seafood",
                "No spicy food",
                "Diabetic-friendly"
            ]
        )
        
        allergies = st.text_input("Food allergies:", placeholder="e.g., nuts, shellfish, eggs")
        dietary_notes = st.text_area("Additional dietary notes:", placeholder="Any other dietary requirements or preferences...")
        
        # Budget & Duration
        st.subheader("💰 Budget & Trip Duration")
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.number_input("Trip Duration (days)", min_value=1, max_value=14, value=3)
            budget_type = st.radio("Budget is per:", ["Person per day", "Group per day", "Total trip"])
        
        with col2:
            budget_min = st.number_input("Minimum Budget (HKD)", min_value=0, value=500)
            budget_max = st.number_input("Maximum Budget (HKD)", min_value=0, value=1500)
        
        # Transportation Preferences
        st.subheader("🚇 Transportation Preferences")
        transport_prefs = st.multiselect(
            "Preferred transportation methods:",
            [
                "MTR (subway)",
                "Bus",
                "Taxi",
                "Private car/van",
                "Ferry",
                "Tram",
                "Walking (short distances)",
                "Accessible tour bus"
            ],
            default=["MTR (subway)", "Taxi"]
        )
        
        # Interests & Preferences
        st.subheader("🎯 Interests & Preferences")
        interests = st.multiselect(
            "What interests you most?",
            [
                "Museums & Culture",
                "Food & Dining",
                "Shopping",
                "Nature & Parks",
                "Temples & Religious Sites",
                "Architecture & Skyline",
                "Markets & Street Food",
                "Entertainment & Shows",
                "Photography spots",
                "Local experiences"
            ]
        )
        
        # Special Requirements
        special_requirements = st.text_area(
            "Special requirements or preferences:",
            placeholder="Any other specific needs, preferences, or things to avoid..."
        )
        
        # Submit button
        if st.button("🎯 Generate My Custom Itinerary", use_container_width=True, type="primary"):
            # Build comprehensive prompt from form data
            prompt_parts = [
                f"Create a detailed {duration}-day Hong Kong itinerary for:"
            ]
            
            # Family composition
            family_desc = []
            if adults > 0:
                family_desc.append(f"{adults} adult{'s' if adults > 1 else ''}")
            if seniors > 0:
                family_desc.append(f"{seniors} senior{'s' if seniors > 1 else ''} (65+)")
            if children > 0:
                child_desc = f"{children} child{'ren' if children > 1 else ''}"
                if 'child_ages' in locals() and child_ages:
                    child_desc += f" (ages: {child_ages})"
                family_desc.append(child_desc)
            
            prompt_parts.append(f"- Group: {', '.join(family_desc)}")
            
            # Mobility requirements
            if mobility_needs:
                prompt_parts.append(f"- Mobility needs: {', '.join(mobility_needs)}")
            if mobility_notes:
                prompt_parts.append(f"- Mobility notes: {mobility_notes}")
            
            # Dietary requirements
            if dietary_prefs:
                prompt_parts.append(f"- Dietary preferences: {', '.join(dietary_prefs)}")
            if allergies:
                prompt_parts.append(f"- Food allergies: {allergies}")
            if dietary_notes:
                prompt_parts.append(f"- Dietary notes: {dietary_notes}")
            
            # Budget
            budget_desc = f"HKD {budget_min}-{budget_max} {budget_type.lower()}"
            prompt_parts.append(f"- Budget: {budget_desc}")
            
            # Transportation
            if transport_prefs:
                prompt_parts.append(f"- Preferred transportation: {', '.join(transport_prefs)}")
            
            # Interests
            if interests:
                prompt_parts.append(f"- Main interests: {', '.join(interests)}")
            
            # Special requirements
            if special_requirements:
                prompt_parts.append(f"- Special requirements: {special_requirements}")
            
            prompt_parts.append("\nPlease provide:")
            prompt_parts.append("- Day-by-day detailed itinerary")
            prompt_parts.append("- Specific venue recommendations with accessibility details")
            prompt_parts.append("- Transportation instructions between locations")
            prompt_parts.append("- Cost estimates for activities and meals")
            prompt_parts.append("- Timing and pacing recommendations")
            prompt_parts.append("- Explanations for why each recommendation suits the group's needs")
            
            return "\n".join(prompt_parts)
    
    return None

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
        st.success("✅ DeepSeek-V3 Connected")
        st.info(f"Model: {MODEL_NAME}")
        
        st.divider()
        
        st.header("🎯 Accessibility Focus")
        st.markdown("""
        **Specialized in:**
        - ♿ Wheelchair accessibility
        - 🍽️ Dietary accommodations
        - 👴 Senior-friendly pacing
        - 👨‍👩‍👧‍👦 Family-friendly options
        - 💰 Budget-conscious planning
        """)
        
        st.divider()
        
        if st.button("🔄 New Conversation"):
            st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
            st.rerun()
        
        st.header("📊 Session Info")
        st.write(f"Messages: {len(st.session_state.messages)}")
    
    # Quick options and custom form (only show if conversation is new)
    if len(st.session_state.messages) <= 1:
        # Quick options
        quick_prompt = create_quick_options()
        if quick_prompt:
            # Process the quick option as if user typed it
            user_message = ChatMessage(
                role="user",
                content=quick_prompt,
                timestamp=datetime.now()
            )
            st.session_state.messages.append(user_message)
            st.rerun()
        
        st.markdown("---")
        
        # Custom detailed form
        custom_prompt = create_custom_form()
        if custom_prompt:
            # Process the custom form as if user typed it
            user_message = ChatMessage(
                role="user",
                content=custom_prompt,
                timestamp=datetime.now()
            )
            st.session_state.messages.append(user_message)
            st.rerun()
    
    # Display conversation
    for message in st.session_state.messages:
        display_message(message)
    
    # Chat input
    if prompt := st.chat_input("Or describe your specific Hong Kong travel needs..."):
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