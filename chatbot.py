import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Chatbot")
st.title("AI Chatbot")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display chat
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
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # ✅ THIS WORKS
            messages=st.session_state.chat_history
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
