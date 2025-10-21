import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1e1e2f, #2e2e47);
        color: #fff;
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background: transparent;
    }
    .stChatMessage {
        border-radius: 15px !important;
        padding: 10px 15px;
        margin: 5px 0;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #0059b3;
        color: white;
        align-self: flex-end;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #2f2f4f;
        color: #ffffff;
        align-self: flex-start;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0059b3, #0099ff);
        color: white;
        border-radius: 10px;
        padding: 5px 20px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #007acc, #33ccff);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>💬 ChatBot Curhat</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ccc;'>Powered by Gemini & LangChain</p>", unsafe_allow_html=True)


def get_api_key_input():
    if "GOOGLE_API_KEY" not in st.session_state:
        st.session_state["GOOGLE_API_KEY"] = ""

    if st.session_state["GOOGLE_API_KEY"]:
        return

    with st.expander("🔑 Masukkan Google API Key", expanded=True):
        api_key = st.text_input("Google API Key", type="password", placeholder="Masukkan API Key di sini...")
        submit = st.button("Submit Key")

        if submit:
            if not api_key:
                st.error("API Key tidak boleh kosong!")
            else:
                st.session_state["GOOGLE_API_KEY"] = api_key
                os.environ["GOOGLE_API_KEY"] = api_key
                st.success("API Key tersimpan!")
                st.rerun()

    if not st.session_state["GOOGLE_API_KEY"]:
        st.stop()



def load_llm():
    if "llm" not in st.session_state:
        st.session_state["llm"] = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    return st.session_state["llm"]



def get_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    return st.session_state["chat_history"]


def display_chat_message(message):
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)


def display_chat_history(chat_history):
    for chat in chat_history:
        display_chat_message(chat)


def user_query_to_llm(llm, chat_history):
    prompt = st.chat_input("Ketik pesan di sini...")
    if not prompt:
        st.stop()
    chat_history.append(HumanMessage(content=prompt))
    display_chat_message(chat_history[-1])

    with st.spinner("Sedang berpikir... 🤔"):
        response = llm.invoke(chat_history)
    chat_history.append(response)
    display_chat_message(chat_history[-1])


def main():
    get_api_key_input()
    llm = load_llm()
    chat_history = get_chat_history()
    display_chat_history(chat_history)
    user_query_to_llm(llm, chat_history)


if __name__ == "__main__":
    main()
