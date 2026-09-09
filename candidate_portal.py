import requests
import streamlit as st
from interview_evaluator import evaluate_interview
# ---------------- Interview ID ----------------

interview_id = st.query_params.get("interview_id")


# ---------------- Load Interview ----------------

if not interview_id:

    st.error("❌ Invalid interview link.")

    st.stop()


response = requests.get(
    f"http://127.0.0.1:8000/interviews/{interview_id}"
)

if response.status_code != 200:

    st.error("❌ Interview not found.")

    st.stop()


interview = response.json()


# ---------------- Interview Data ----------------

candidate_name = interview["candidate"]
interview_date = interview["date"]
interview_mode = interview["mode"]
questions = interview["questions"]


# ---------------- Page Configuration ----------------

st.set_page_config(
    page_title="TalentMatch AI - Interview Portal",
    page_icon="🎤",
    layout="centered"
)


st.title("🤖 TalentMatch AI")
st.subheader("🎤 Interview Portal")

st.divider()

st.header(f"Welcome, {candidate_name}! 👋")

st.write(
    "You have been invited to complete an interview through TalentMatch AI."
)

st.info(
    "Please read the instructions carefully before starting your interview."
)

st.markdown("### 📋 Interview Instructions")

st.write("✅ Make sure you have a stable internet connection.")
st.write("✅ Find a quiet environment.")
st.write("✅ Make sure your microphone is working.")
st.write("✅ Read each question carefully.")
st.write("✅ Take your time and answer clearly.")

st.divider()

st.markdown("### 📅 Interview Details")

st.write(f"**Candidate:** {candidate_name}")
st.write(f"**Date:** {interview_date}")
st.write(f"**Mode:** {interview_mode}")

st.divider()


# ---------------- Start Interview ----------------

if "interview_started" not in st.session_state:

    st.session_state.interview_started = False


if st.button("🎤 Start Interview"):

    st.session_state.interview_started = True


if st.session_state.interview_started:

    st.success("✅ Interview started!")

    # --------------------------
    # Current Question
    # --------------------------

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    current_question = st.session_state.current_question

    st.markdown(
        f"### 🎤 Question {current_question + 1} of {len(questions)}"
    )

    st.write(questions[current_question])

    # --------------------------
    # Candidate Answer
    # --------------------------

    answer = st.text_area(
        "📝 Your Answer",
        key=f"answer_{current_question}",
        height=150
    )

    # --------------------------
    # Next Question
    # --------------------------

    if current_question < len(questions) - 1:

        if st.button("Next →"):

            st.session_state.answers[current_question] = answer

            st.session_state.current_question += 1

            st.rerun()

    else:

        if st.button("🏁 Submit Interview"):

            st.session_state.answers[current_question] = answer

            with st.spinner("🤖 Evaluating your interview..."):

                evaluation = evaluate_interview(
                    questions,
                    st.session_state.answers
                )

            st.success("🎉 Interview submitted successfully!")

            st.markdown("### 📊 Interview Evaluation")

            st.write(evaluation)