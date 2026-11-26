
import streamlit as st
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Application title
st.title("🤖 My AI Chatbot")
st.caption("Powered by Streamlit, LangChain and Groq")

# Check API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found. Check your .env file.")
    st.stop()

# Initialize the Groq model
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=api_key
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Convert chat history into LangChain messages
    chat_history = []

    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_history.append(
                HumanMessage(content=message["content"])
            )
        else:
            chat_history.append(
                AIMessage(content=message["content"])
            )

    # Add system instructions
    messages = [
        SystemMessage(
            content="You are a friendly and helpful AI assistant. "
                    "Answer questions clearly and simply."
        )
    ] + chat_history

    # Generate AI response
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = llm.invoke(messages)

                answer = response.content

                st.markdown(answer)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Something went wrong: {e}")
s