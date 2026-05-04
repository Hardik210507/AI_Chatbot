import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Chatbot")
st.title("AI Chatbot")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # show user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        st.error(e)
        reply = "Something went wrong"

    # show bot reply
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
