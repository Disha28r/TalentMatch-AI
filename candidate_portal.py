import requests
import streamlit as st
import whisper
import hashlib
from audio_recorder_streamlit import audio_recorder
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
    
if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False


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
        
    if "transcripts" not in st.session_state:
        st.session_state.transcripts = {}
        
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None

    current_question = st.session_state.current_question

    st.markdown(
        f"### 🎤 Question {current_question + 1} of {len(questions)}"
    )

    st.write(questions[current_question])
    st.write("🎙️ Or answer by speaking:")

    audio = audio_recorder(
    text="🎙️ Record Answer",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x"
    )

    if audio:
        audio_hash = hashlib.md5(audio).hexdigest()

        if audio_hash != st.session_state.last_audio_hash:

            st.session_state.last_audio_hash = audio_hash

            with st.spinner("🤖 Transcribing your answer..."):
                model = whisper.load_model("base")

                with open("answer.wav", "wb") as f:
                    f.write(audio)

                result = model.transcribe("answer.wav")

            transcript = result["text"]

            st.session_state.transcripts[current_question] = transcript
            st.session_state[f"answer_{current_question}"] = transcript

            st.success("✅ Transcription complete!")


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

            next_question = st.session_state.current_question

            st.session_state[f"answer_{next_question}"] = ""
            st.session_state.transcripts[next_question] = ""

            st.rerun()

    else:

        if not st.session_state.interview_completed:

            if st.button("🏁 Submit Interview"):
                st.session_state.answers[current_question] = answer
                st.session_state.interview_completed = True

                with st.spinner("🤖 Evaluating your interview..."):

                    evaluation = evaluate_interview(
                        questions,
                        st.session_state.answers
                    )

                    evaluation_response = requests.put(
                        f"http://127.0.0.1:8000/interviews/{interview_id}/evaluation",
                        json=evaluation.model_dump()
                    )

                if evaluation_response.status_code == 200:
                    st.success("🎉 Interview submitted successfully!")
                else:
                    st.error("❌ Failed to save interview evaluation.")
                    st.write(evaluation_response.text)

                st.markdown("## 📊 Interview Evaluation")

                st.metric(
                    "Overall Score",
                    f"{evaluation.overall_score} / 100"
                )

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Technical Knowledge",
                        f"{evaluation.technical_knowledge} / 100"
                    )

                with col2:
                    st.metric(
                        "Communication",
                        f"{evaluation.communication} / 100"
                    )

                with col3:
                    st.metric(
                        "Problem Solving",
                        f"{evaluation.problem_solving} / 100"
                    )

                st.divider()

                st.markdown("### 💪 Strengths")

                for strength in evaluation.strengths:
                    st.write(f"• {strength}")

                st.markdown("### 📈 Areas for Improvement")

                for area in evaluation.areas_for_improvement:
                    st.write(f"• {area}")

                st.markdown("### 🎯 Recommendation")

                st.info(evaluation.recommendation)

                st.markdown("### 💬 Brief Feedback")

                st.write(evaluation.brief_feedback)