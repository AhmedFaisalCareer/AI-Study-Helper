```python
import streamlit as st
import requests
from google import genai


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="🤖 AI Study Helper",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# SETTINGS
# ==========================================

FIREBASE_URL = "https://ai-study-helper-69c91-default-rtdb.firebaseio.com"

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# FIREBASE - SAVE PROFILE
# ==========================================

def save_profile(student_id, profile):

    url = f"{FIREBASE_URL}/students/{student_id}/profile.json"

    response = requests.put(
        url,
        json=profile
    )

    st.write("Firebase status:", response.status_code)
    st.write("Firebase response:", response.text)

    if response.status_code == 200:
        return True

    return False


# ==========================================
# FIREBASE - GET PROFILE
# ==========================================

def get_profile(student_id):

    url = f"{FIREBASE_URL}/students/{student_id}/profile.json"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        return data

    return None


# ==========================================
# FIREBASE - SAVE MESSAGE
# ==========================================

def save_message(student_id, question, answer):

    url = f"{FIREBASE_URL}/students/{student_id}/history.json"

    data = {
        "question": question,
        "answer": answer
    }

    response = requests.post(
        url,
        json=data
    )

    if response.status_code == 200:
        return True

    st.write("Firebase history error:")
    st.write(response.status_code)
    st.write(response.text)

    return False


# ==========================================
# FIREBASE - GET HISTORY
# ==========================================

def get_history(student_id):

    url = f"{FIREBASE_URL}/students/{student_id}/history.json"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        if data:

            history = []

            for key in data:

                item = data[key]

                history.append({
                    "question": item.get("question", ""),
                    "answer": item.get("answer", "")
                })

            return history

    return []


# ==========================================
# FIREBASE - CLEAR HISTORY
# ==========================================

def clear_history(student_id):

    url = f"{FIREBASE_URL}/students/{student_id}/history.json"

    response = requests.delete(url)

    if response.status_code == 200:
        return True

    return False


# ==========================================
# SESSION STATE
# ==========================================

if "profile" not in st.session_state:
    st.session_state.profile = None

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# PROFILE PAGE
# ==========================================

if st.session_state.profile is None:

    st.title("👋 Welcome to AI Study Helper")

    st.write(
        "Before you start studying, please create your student profile."
    )

    st.divider()

    st.subheader("👤 Student Profile")

    student_id = st.text_input(
        "Student ID / Username",
        placeholder="Example: ahmed123"
    )

    name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )

    student_class = st.selectbox(
        "Your Class / Grade",
        [
            "Class 6",
            "Class 7",
            "Class 8",
            "Class 9",
            "Class 10",
            "O Level",
            "A Level",
            "Other"
        ]
    )

    school = st.text_input(
        "School Name",
        placeholder="Enter your school name"
    )

    subject = st.selectbox(
        "Main Subject",
        [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "English",
            "Geography",
            "History",
            "Islamiat",
            "Other"
        ]
    )

    learning_goal = st.selectbox(
        "What do you want help with?",
        [
            "Homework",
            "Exam Preparation",
            "Understanding Concepts",
            "Making Notes",
            "Practice Questions",
            "Revision"
        ]
    )

    st.divider()

    if st.button(
        "🚀 Start Studying",
        use_container_width=True
    ):

        if student_id == "":

            st.warning(
                "Please enter a Student ID."
            )

        elif name == "":

            st.warning(
                "Please enter your name."
            )

        elif school == "":

            st.warning(
                "Please enter your school name."
            )

        else:

            student_id = (
                student_id
                .strip()
                .lower()
                .replace(" ", "_")
            )

            # Check if student already exists

            old_profile = get_profile(
                student_id
            )


            # ==================================
            # RETURNING STUDENT
            # ==================================

            if old_profile:

                st.session_state.profile = old_profile
                st.session_state.student_id = student_id

                old_history = get_history(
                    student_id
                )

                st.session_state.messages = []

                for item in old_history:

                    st.session_state.messages.append({
                        "role": "user",
                        "content": item["question"]
                    })

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": item["answer"]
                    })

                st.success(
                    "Welcome back! Your previous history has been loaded."
                )

                st.rerun()


            # ==================================
            # NEW STUDENT
            # ==================================

            else:

                profile = {
                    "name": name,
                    "class": student_class,
                    "school": school,
                    "subject": subject,
                    "goal": learning_goal
                }

                saved = save_profile(
                    student_id,
                    profile
                )


                if saved:

                    st.session_state.profile = profile
                    st.session_state.student_id = student_id
                    st.session_state.messages = []

                    st.success(
                        "Profile saved successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Could not save your profile to Firebase."
                    )


# ==========================================
# MAIN AI STUDY HELPER
# ==========================================

else:

    profile = st.session_state.profile

    student_id = st.session_state.student_id


    # ======================================
    # HEADER
    # ======================================

    st.title("🤖 AI Study Helper")

    st.write(
        f"Welcome, **{profile['name']}**! "
        f"Let's study **{profile['subject']}** together."
    )


    # ======================================
    # SIDEBAR
    # ======================================

    with st.sidebar:

        st.header("👤 Student Profile")

        st.write(
            f"**Name:** {profile['name']}"
        )

        st.write(
            f"**Class:** {profile['class']}"
        )

        st.write(
            f"**School:** {profile['school']}"
        )

        st.write(
            f"**Subject:** {profile['subject']}"
        )

        st.write(
            f"**Goal:** {profile['goal']}"
        )

        st.divider()


        if st.button(
            "🔄 Change Profile",
            use_container_width=True
        ):

            st.session_state.profile = None
            st.session_state.student_id = None
            st.session_state.messages = []

            st.rerun()


        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            deleted = clear_history(
                student_id
            )

            if deleted:

                st.session_state.messages = []

                st.success(
                    "History cleared."
                )

                st.rerun()

            else:

                st.error(
                    "Could not clear history."
                )


    # ======================================
    # AI OPTIONS
    # ======================================

    output_type = st.selectbox(
        "Choose output type",
        [
            "Summary",
            "Quiz",
            "Detailed Notes",
            "Mind Map"
        ]
    )

    difficulty = st.selectbox(
        "Choose difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


    # ======================================
    # CHAT INPUT
    # ======================================

    user_message = st.chat_input(
        "Ask something about your study topic..."
    )


    if user_message:

        # Save question to current session

        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })


        # ==================================
        # GET LAST CONVERSATION FROM FIREBASE
        # ==================================

        history = get_history(
            student_id
        )

        last_question = ""
        last_answer = ""


        if history:

            last_question = history[-1]["question"]
            last_answer = history[-1]["answer"]


        # ==================================
        # AI PROMPT
        # ==================================

        prompt = f"""
You are an AI Study Helper.

STUDENT PROFILE

Name: {profile['name']}
Class: {profile['class']}
School: {profile['school']}
Subject: {profile['subject']}
Learning Goal: {profile['goal']}


PREVIOUS CONVERSATION

Previous Question:
{last_question}

Previous Answer:
{last_answer}


CURRENT QUESTION

{user_message}


OUTPUT SETTINGS

Output Type: {output_type}
Difficulty: {difficulty}


INSTRUCTIONS

1. Answer the current question clearly.
2. Adjust the answer to the student's class level.
3. Use simple language when possible.
4. Remember the previous question and answer.
5. If the student refers to the previous question,
   use the previous conversation to understand it.
6. Do not unnecessarily repeat the previous answer.
7. For Summary, use important points.
8. For Quiz, create questions and answers.
9. For Detailed Notes, use headings and bullet points.
10. For Mind Map, create a clear text hierarchy.
11. Help the student understand the topic.

Answer the current question now.
"""


        # ==================================
        # GEMINI
        # ==================================

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        answer = response.text


        # ==================================
        # DISPLAY ANSWER
        # ==================================

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


        # ==================================
        # SAVE TO FIREBASE
        # ==================================

        save_message(
            student_id,
            user_message,
            answer
        )


    # ======================================
    # DISPLAY CHAT HISTORY
    # ======================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # ======================================
    # ABOUT
    # ======================================

    st.divider()

    st.subheader("ℹ️ About")

    st.write(
        "🤖 AI Study Helper helps students study any topic "
        "using AI. Student profiles and study history are "
        "saved in Firebase so the AI can remember previous "
        "questions and answers."
    )
```
