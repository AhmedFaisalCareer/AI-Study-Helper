import streamlit as st
from google import genai

st.set_page_config(
    page_title="📚AI Study Helper",
    layout="wide"
)

st.title("📚AI Study Helper")
st.write("Study any topic using AI.")

topic = st.text_input(
    "Enter a study topic",
    placeholder="Example: Photosynthesis"
)

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

if st.button("Generate"):
    if topic == "":
        st.warning("Please enter a study topic.")
    else:
        prompt = f"""
Topic: {topic}
Output type: {output_type}
Difficulty: {difficulty}

Create useful study material for the student.
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        st.subheader(output_type)
        st.write(response.text)
