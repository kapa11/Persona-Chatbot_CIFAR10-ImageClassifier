import streamlit as st
import os
import json
import textwrap
from datetime import datetime
from huggingface_hub import InferenceClient
from typing import List, Dict, Any

class PersonaChatBot:
    def __init__(self):
        # Initialize HuggingFace client
        self.hf_token = os.environ.get("HF_TOKEN")
        if not self.hf_token:
            raise ValueError("HF_TOKEN environment variable is required")
        
        self.client = InferenceClient(
            provider="cerebras",
            api_key=self.hf_token,
        )
        
        # Persona definitions
        self.personas = {
            "RoastBot": {
                "description": "Always responds with witty or sarcastic roasts",
                "system_prompt": "You are RoastBot, a witty and sarcastic AI that roasts users with clever humor. Always respond with playful roasts and sarcastic comments, but keep it light-hearted and fun. Never be genuinely mean or offensive. You have access to the entire conversation history from other personas in this chat session - use this information to make clever references and roasts."
            },
            "ShakespeareBot": {
                "description": "Responds in old-English, Shakespeare-style prose",
                "system_prompt": "Thou art a learned bot, speaking only in the flowery tongue of Shakespeare's era. Respond to all queries with elaborate Elizabethan English, using 'thou', 'thee', 'thy', 'hath', 'doth', and similar archaic terms. Make thy responses poetic and grandiose. Thou hast access to all previous conversations from other personas in this session - reference them in thy eloquent speech."
            },
            "EmojiBot": {
                "description": "Converts everything into emoji-speak",
                "system_prompt": "You are EmojiBot! 😄 Respond to everything using lots of emojis and convert text into emoji representations whenever possible. Use emojis to express emotions, objects, actions, and concepts. Make your responses fun and colorful with emojis! 🌈✨ You can see all previous conversations from other personas in this session - reference them with emojis!"
            },
            "PhilosopherBot": {
                "description": "Responds with deep philosophical insights and questions",
                "system_prompt": "You are PhilosopherBot, a contemplative AI that turns every conversation into deep philosophical discourse. Always respond with profound insights, thought-provoking questions, and references to great philosophers. Make users question the nature of reality, existence, and meaning. You have access to all conversations from other personas in this session - use them to create deeper philosophical connections. Like the greek philosopher Socrates"
            },
            "PirateBot": {
                "description": "Talks like a swashbuckling pirate like Captain Jack Sparrow",
                "system_prompt": "Ahoy! You be PirateBot, a swashbuckling AI that speaks like a proper pirate! Use 'ahoy', 'matey', 'arr', 'ye', 'yer', and other pirate terminology. Talk about treasure, the seven seas, and adventures. Make every response sound like it came from a pirate ship! Ye can see all previous conversations from other personas in this session - use 'em to spin great tales, matey! Be like Captain Jack Sparrow from the Pirates of the Caribbean Universe"
            }
        }
        
        self.max_history = 30 #The latest number of exchanges stored in context to respond accordingly

    def initialize_session_state(self):
        """Initialize all session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "current_persona" not in st.session_state:
            st.session_state.current_persona = "RoastBot"
        
        if "global_conversation_history" not in st.session_state:
            st.session_state.global_conversation_history = []

    def add_to_global_history(self, user_message: str, bot_response: str, persona_name: str):
        """Add conversation to SHARED global history with memory management"""
        st.session_state.global_conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "persona": persona_name,
            "user": user_message,
            "bot": bot_response
        })
        
        # Keep only recent conversations to manage context length
        if len(st.session_state.global_conversation_history) > self.max_history:
            st.session_state.global_conversation_history = st.session_state.global_conversation_history[-self.max_history:]

    def build_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Build messages array with system prompt and GLOBAL conversation history"""
        messages = []
        
        current_persona = st.session_state.current_persona
        
        # Add system prompt for current persona
        messages.append({
            "role": "system",
            "content": self.personas[current_persona]["system_prompt"]
        })
        
        # Add GLOBAL conversation history (from ALL personas) for context
        for exchange in st.session_state.global_conversation_history[-20:]:  # Last 10 exchanges from any persona
            # Format the message to show which persona spoke
            persona_indicator = f"[Previous conversation with {exchange['persona']}]" if exchange['persona'] != current_persona else ""
            
            user_content = f"{persona_indicator} {exchange['user']}" if persona_indicator else exchange['user']
            bot_content = exchange['bot']
            
            messages.append({"role": "user", "content": user_content})
            messages.append({"role": "assistant", "content": bot_content})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages

    def get_bot_response(self, user_input: str) -> str:
        """Get response from the bot"""
        try:
            messages = self.build_messages(user_input)
            
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                max_tokens=700,
                temperature=0.7
            )
            
            return completion.choices[0].message.content.strip()
        
        except Exception as e:
            return f"🚨 Oops! I encountered an error: {str(e)}"

    def clear_all_memory(self):
        """Clear ALL shared conversation memory"""
        st.session_state.global_conversation_history = []
        st.session_state.messages = []

    def export_conversations(self):
        """Export all conversation data to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chatbot_global_conversations_{timestamp}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "session_type": "shared_memory_across_personas",
            "personas": self.personas,
            "global_conversation_history": st.session_state.global_conversation_history,
            "total_exchanges": len(st.session_state.global_conversation_history)
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            return None

def main():
    # Page configuration
    st.set_page_config(
        page_title="Kapa's Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .model-info {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .persona-info {
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
        color: #1f3869
    }
    .memory-info {
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #1f3869
    }
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .stChatMessage {
        margin-bottom: 1rem;
    }
    .stChatMessage > div {
        border-radius: 15px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize chatbot
    try:
        chatbot = PersonaChatBot()
        chatbot.initialize_session_state()
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("💡 Please set your HF_TOKEN environment variable")
        st.stop()

    # Header
    st.markdown('<h1 class="main-header">🤖 Kapa\'s Chatbot</h1>', unsafe_allow_html=True)

    # Sidebar for persona selection and controls
    with st.sidebar:
        st.header("🎭 Persona Selection")
        
        current_persona = st.selectbox(
            "Choose Your AI Persona:",
            list(chatbot.personas.keys()),
            index=list(chatbot.personas.keys()).index(st.session_state.current_persona),
            key="persona_selector"
        )
        
        # Update session state if persona changed
        if current_persona != st.session_state.current_persona:
            st.session_state.current_persona = current_persona
            st.rerun()
        
        # Display current persona info
        st.markdown(f"""
        <div class="persona-info">
            <strong>🎯 Active: {current_persona}</strong><br>
            <em>{chatbot.personas[current_persona]["description"]}</em>
        </div>
        """, unsafe_allow_html=True)

        # Memory status
        memory_count = len(st.session_state.global_conversation_history)
        st.markdown(f"""
        <div class="memory-info">
            <strong>🧠 Shared Memory:</strong> {memory_count} messages<br>
            <em>All personas can access this conversation history</em>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Control buttons
        st.header("🔧 Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Memory", use_container_width=True):
                chatbot.clear_all_memory()
                st.success("Memory cleared!")
                st.rerun()
        
        with col2:
            if st.button("💾 Export Chat", use_container_width=True):
                filename = chatbot.export_conversations()
                if filename:
                    st.success(f"Exported to {filename}")
                else:
                    st.error("Export failed!")

        # Statistics
        if st.session_state.global_conversation_history:
            st.header("📊 Statistics")
            
            # Count by persona
            persona_counts = {}
            for exchange in st.session_state.global_conversation_history:
                persona = exchange["persona"]
                persona_counts[persona] = persona_counts.get(persona, 0) + 1
            
            st.write("**Messages by Persona:**")
            for persona, count in persona_counts.items():
                st.write(f"• {persona}: {count}")
            
            total_chars = sum(len(ex["user"]) + len(ex["bot"]) for ex in st.session_state.global_conversation_history)
            st.write(f"**Total Characters:** {total_chars:,}")

    # Main chat area
    st.header(f"💬 Chatting with {current_persona}")

    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        # Display all messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
                if message["role"] == "assistant":
                    st.markdown(f"**{message.get('persona', 'Bot')}:** {message['content']}")
                else:
                    st.write(message["content"])

    # Chat input (this stays at the bottom)
    if prompt := st.chat_input("💭 Type your message here..."):
        # Handle quit command
        if prompt.lower().strip() == 'quit':
            st.info("👋 Thanks for chatting! Refresh the page to start a new session.")
            st.balloons()
            st.stop()

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)

        # Get bot response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner(f"{current_persona} is thinking..."):
                response = chatbot.get_bot_response(prompt)
            
            st.markdown(f"**{current_persona}:** {response}")

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "persona": current_persona
        })

        # Add to global memory
        chatbot.add_to_global_history(prompt, response, current_persona)

        # Rerun to update the display
        st.rerun()

    # Footer info
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"🎯 **Current Persona:** {current_persona}")
    
    with col2:
        st.info(f"💬 **Messages:** {len(st.session_state.messages)}")
    
    with col3:
        st.info(f"🧠 **Memory:** {len(st.session_state.global_conversation_history)} exchanges")

if __name__ == "__main__":
    main()
