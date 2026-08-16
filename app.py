import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Helper",
    layout="wide"
)

st.title("AI Study Helper")
st.write("Study any topic using AI.")

if "topics" not in st.session_state:
    st.session_state.topics = []

search = st.text_input(
    "Search previous topics",
    placeholder="Search for a topic..."
)

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
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.session_state.topics.append({
            "topic": topic,
            "output_type": output_type,
            "difficulty": difficulty,
            "response": response.text
        })

        st.subheader(output_type)
        st.write(response.text)

st.subheader("Previous Topics")

if search == "":
    topics_to_show = st.session_state.topics
else:
    topics_to_show = []

    for item in st.session_state.topics:
        if search.lower() in item["topic"].lower():
            topics_to_show.append(item)

if len(topics_to_show) == 0:
    st.write("No previous topics found.")
else:
    for item in topics_to_show:
        st.write("Topic:", item["topic"])
        st.write("Type:", item["output_type"])
        st.write("Difficulty:", item["difficulty"])
        st.write(item["response"])
        st.divider()

st.subheader("About")

st.write(
    "AI Study Helper is a web app that helps students study any topic "
    "using AI. Students can enter a topic, choose an output type and "
    "select a difficulty level."
)
