import streamlit as st
from google import genai

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("🤖 الشات بوت الذكي الخاص بي")
st.write("أهلاً بيك! أنا شات بوت مبني بالذكاء الاصطناعي، اسألني في أي حاجة.")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("من فضلك أضف GEMINI_API_KEY في الإعدادات!")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("اكتب رسالتك هنا...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("جاري التفكير..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        bot_reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
