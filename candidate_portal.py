import streamlit as st


st.set_page_config(
    page_title="TalentMatch AI - Interview Portal",
    page_icon="🎤",
    layout="centered"
)

st.title("🤖 TalentMatch AI")
st.subheader("🎤 Interview Portal")

st.divider()

candidate_name = "Disha"
interview_date = "14 August 2026"
interview_mode = "Online"
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

questions = [
    "Tell us about yourself.",
    "Describe your experience with Python.",
    "How would you design an AI application?",
    "Tell us about a challenging project you worked on.",
    "Why are you interested in this role?"
]

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if st.button("🎤 Start Interview"):

    st.session_state.interview_started = True


if st.session_state.interview_started:

    st.success("✅ Interview started!")

    st.markdown("### 🎤 Interview Questions")

    for i, question in enumerate(questions, start=1):

        st.write(f"**Q{i}.** {question}")