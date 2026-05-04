import streamlit as st
from groq import Groq

# Page config
st.set_page_config(page_title="AI Chatbot")
st.title("AI Chatbot")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        # Send request to Groq
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ working model
            messages=st.session_state.chat_history
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"Error: {e}"

    # Store assistant reply
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)
