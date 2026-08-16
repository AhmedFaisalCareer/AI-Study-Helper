import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Helper",
    layout="wide"
)

st.title("AI Study Helper")
st.write("Ask questions and study any topic using AI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

output_type = st.selectbox(
    "Choose output type",
    ["Summary", "Quiz", "Detailed Notes", "Mind Map"]
)

difficulty = st.selectbox(
    "Choose difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY is missing. Please add it in Streamlit Secrets.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

user_message = st.chat_input("Ask something about your study topic...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    prompt = f"""
You are an AI Study Helper.

The student is studying:
{user_message}

Output type:
{output_type}

Difficulty:
{difficulty}

Give a clear and useful answer for the student.
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.subheader("About")

st.write(
    "AI Study Helper is a web app that helps students study any topic "
    "using AI. Students can ask questions, choose an output type and "
    "select a difficulty level."
)
