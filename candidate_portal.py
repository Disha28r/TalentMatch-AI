import json
import streamlit as st

# ---------------- Interview ID ----------------

interview_id = st.query_params.get("interview_id")


# ---------------- Load Interview ----------------

if not interview_id:

    st.error("❌ Invalid interview link.")

    st.stop()


with open("interviews.json", "r") as file:

    interviews = json.load(file)


if interview_id not in interviews:

    st.error("❌ Interview not found.")

    st.stop()


interview = interviews[interview_id]


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

    st.markdown("### 🎤 Interview Questions")

    for i, question in enumerate(questions, start=1):

        st.write(f"**Q{i}.** {question}")