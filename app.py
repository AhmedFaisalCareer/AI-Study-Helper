import streamlit as st
from google import genai
import json

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="📚"
)

st.title("📚 AI Quiz Generator")
st.subheader("Generate quizzes with AI")

st.write(
    "Create a personalized quiz by choosing a topic, "
    "quiz type, difficulty, and number of questions."
)

# Put your Gemini API key here
api_key = "Gemini API key 

# Create Gemini client
client = genai.Client(api_key=api_key)


subject = st.text_input(
    "📖 Enter your subject or topic",
    placeholder="Example: Photosynthesis"
)

quiz_type = st.selectbox(
    "📝 Select quiz type",
    [
        "Multiple Choice",
        "True/False",
        "Fill in the Blank"
    ]
)

difficulty = st.selectbox(
    "🎯 Select difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

num_questions = st.number_input(
    "🔢 Number of questions",
    min_value=1,
    max_value=20,
    value=5
)


if st.button("🚀 Generate Quiz", use_container_width=True):

    if subject.strip() == "":
        st.warning("⚠️ Please enter a subject or topic.")

    else:

        prompt = f"""
Create a {difficulty} level {quiz_type} quiz about {subject}.

Create exactly {num_questions} questions.

Return ONLY valid JSON.

For Multiple Choice:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option"
        }}
    ]
}}

For True/False:

{{
    "questions": [
        {{
            "question": "Question text",
            "answer": "True"
        }}
    ]
}}

For Fill in the Blank:

{{
    "questions": [
        {{
            "question": "Question with a blank",
            "answer": "Correct answer"
        }}
    ]
}}

Do not add markdown.
Do not add explanations.
Return only JSON.
"""

        with st.spinner("🤖 Generating your quiz..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )

                result = response.text.strip()

                if result.startswith("```json"):
                    result = result[7:]

                if result.startswith("```"):
                    result = result[3:]

                if result.endswith("```"):
                    result = result[:-3]

                result = result.strip()

                quiz_data = json.loads(result)

                st.session_state.quiz = quiz_data
                st.session_state.quiz_type = quiz_type
                st.session_state.subject = subject

                st.success("✅ Quiz generated successfully!")

            except json.JSONDecodeError:

                st.error(
                    "❌ Gemini returned an invalid format. "
                    "Please try again."
                )

            except Exception as e:

                st.error("❌ Something went wrong.")
                st.write(str(e))


if "quiz" in st.session_state:

    st.divider()

    st.header("🧠 Your Quiz")

    st.write(
        f"**Topic:** {st.session_state.subject}"
    )

    st.write(
        f"**Quiz Type:** {st.session_state.quiz_type}"
    )

    quiz_data = st.session_state.quiz
    quiz_type = st.session_state.quiz_type


    for i, question in enumerate(
        quiz_data["questions"]
    ):

        st.subheader(
            f"Question {i + 1}"
        )

        st.write(
            question["question"]
        )


        if quiz_type == "Multiple Choice":

            st.radio(
                "Choose your answer:",
                question["options"],
                key=f"answer_{i}"
            )


        elif quiz_type == "True/False":

            st.radio(
                "Choose your answer:",
                ["True", "False"],
                key=f"answer_{i}"
            )


        elif quiz_type == "Fill in the Blank":

            st.text_input(
                "Your answer:",
                key=f"answer_{i}"
            )


    st.divider()

    with st.expander("🔐 Show Correct Answers"):

        for i, question in enumerate(
            quiz_data["questions"]
        ):

            st.write(
                f"**Question {i + 1}:** "
                f"{question['answer']}"
            )


    if st.button(
        "🔄 Generate Another Quiz",
        use_container_width=True
    ):

        del st.session_state.quiz

        st.rerun()
