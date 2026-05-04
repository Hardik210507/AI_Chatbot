import streamlit as st
from openai import OpenAI

# Page setup
st.set_page_config(page_title="AI Chatbot")
st.title("AI Chatbot")

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    # Store and display user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        # API call
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_prompt
        )

        # Extract response safely
        reply = ""

        if hasattr(response, "output_text") and response.output_text:
            reply = response.output_text
        else:
            reply = response.output[0].content[0].text

    except Exception as e:
        st.error(e)  # show actual error on UI
        reply = "Something went wrong"

    # Store and display bot reply
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
