import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent import MiddlewareAgent
from middleware.logging_middleware import LoggingMiddleware
from middleware.security_middleware import SecurityMiddleware
from middleware.cost_middleware import CostControlMiddleware
from middleware.adaptive_middleware import AdaptiveResponseMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Middleware-Enhanced Chatbot", page_icon="🤖")

st.title("🤖 Middleware-Enhanced Chatbot")
st.markdown("""
This chatbot uses a custom middleware pipeline for:
- **Logging**: Tracking interactions
- **Security**: Redacting PII (emails, phone numbers)
- **Cost Control**: Enforcing token limits
- **Adaptive Behavior**: Based on user profile
""")

# Initialize User Profile in sidebar
st.sidebar.title("User Configuration")
user_id = st.sidebar.selectbox("Select User Profile", ["user_1", "user_2", "default"])
user_profiles = {
    "user_1": {"tier": "premium", "style": "helpful and detailed"},
    "user_2": {"tier": "free", "style": "short and concise"},
    "default": {"tier": "standard", "style": "balanced"}
}

# Setup Agent and Pipeline
@st.cache_resource
def get_agent():
    middlewares = [
        LoggingMiddleware(),
        SecurityMiddleware(),
        CostControlMiddleware(token_limit=2000),
        AdaptiveResponseMiddleware(user_profiles=user_profiles)
    ]
    return MiddlewareAgent(middlewares=middlewares)

agent = get_agent()

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Check for PII locally (optional, middleware also does this but we want to show it in UI)
    # The middleware will redact it before it hits the LLM anyway.
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Prepare history for the agent
        langchain_history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                langchain_history.append(HumanMessage(content=m["content"]))
            else:
                langchain_history.append(AIMessage(content=m["content"]))
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_content = agent.chat(messages=langchain_history, user_id=user_id)
                st.markdown(response_content)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Sidebar info
st.sidebar.divider()
st.sidebar.info(f"Active Session: {user_id}")
if hasattr(agent.pipeline.middlewares[2], 'total_tokens'):
    st.sidebar.metric("Tokens Used", agent.pipeline.middlewares[2].total_tokens)
