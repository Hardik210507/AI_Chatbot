import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Chatbot")
st.title("AI Chatbot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display previous messages
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
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_prompt
        )

        try:
            reply = response.output_text
        except:
            reply = response.output[0].content[0].text

    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)