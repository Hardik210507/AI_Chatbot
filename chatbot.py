import streamlit as st
from google import genai

st.set_page_config(page_title="AI Chatbot")
st.title("AI Chatbot")

client = genai.Client(api_key=st.secrets["API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_prompt
        )

        reply = response.text

    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
