import os
import tempfile
from pathlib import Path

import streamlit as st

from resume_parser import (
    parse_job_description,
    read_resume,
    parse_resume,
    final_score,
     generate_interview_questions,
)

# ---------------- Session State ----------------
if "scheduled_interviews" not in st.session_state:
    st.session_state.scheduled_interviews = []
    
if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = {}
    
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "results" not in st.session_state:
    st.session_state.results = []

if "job" not in st.session_state:
    st.session_state.job = None



st.set_page_config(
    page_title="TalentMatch AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 TalentMatch AI")
st.subheader("AI Resume Screening System")
# ---------------- New Analysis ----------------

if st.button("🔄 New Analysis"):
    st.session_state.analysis_done = False
    st.session_state.results = []
    st.session_state.job = None
    st.rerun()

# ---------------- Inputs ----------------

job_description = st.text_area(
    "📋 Paste Job Description",
    height=250
)

uploaded_resumes = st.file_uploader(
    "📄 Upload Candidate Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# ---------------- Analyze ----------------

if st.button("🚀 Analyze Candidates"):

    if not job_description:
        st.warning("Please paste a job description.")

    elif not uploaded_resumes:
        st.warning("Please upload at least one resume.")

    else:

        with st.spinner("Analyzing resumes... Please wait."):

            if st.session_state.job is None:
                st.session_state.job = parse_job_description(job_description)

            job = st.session_state.job

            if not st.session_state.analysis_done:

                results = []

                for uploaded_file in uploaded_resumes:

                    suffix = Path(uploaded_file.name).suffix

                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_path = Path(temp_file.name)

                    resume_text = read_resume(temp_path)

                    parsed_resume = parse_resume(resume_text)

                    result = final_score(job, parsed_resume)

                    results.append({
                        "name": parsed_resume.name,
                        "score": result.score,
                        "details": result.details,
                        "resume": parsed_resume
                    })

                    os.remove(temp_path)

                    # Sort candidates
                results.sort(key=lambda x: x["score"], reverse=True)

                # Save results in session state
                st.session_state.results = results
                st.session_state.analysis_done = True

# ---------------- Display Results ----------------            

if st.session_state.analysis_done:

            results = st.session_state.results

            top_candidates = results[:2]
            bottom_candidates = results[-2:]

            st.success("✅ Analysis Completed Successfully!")

            st.divider()
            # ===========================
            # Ranking
            # ===========================

            st.header("🏅 Candidate Rankings")

            for rank, candidate in enumerate(results, start=1):

                st.markdown(
                    f"### {rank}. {candidate['name']} — {candidate['score']}%"
                )

                st.progress(candidate["score"] / 100)

            st.divider()
        
        
            # scheduled_interviews = []

            # ===========================
            # Top Candidates
            # ===========================

            st.header("🏆 Top 2 Candidates")

            for candidate in top_candidates:

                st.subheader(candidate["name"])

                st.progress(candidate["score"] / 100)

                st.write(f"### ⭐ Match Score: {candidate['score']}%")

                st.write(candidate["details"])
                if st.button("🎤 Generate Interview Questions", key=f"generate_{candidate['name']}"):
                    with st.spinner("Generating interview questions..."):

                        questions = generate_interview_questions(st.session_state.job,candidate["resume"])

                        st.session_state.generated_questions[candidate["name"]] = questions.questions
                 # --------------------------
                # Display Questions
                # --------------------------

                if candidate["name"] in st.session_state.generated_questions:

                    st.markdown("### 🎤 Interview Questions")

                    for i, question in enumerate( st.session_state.generated_questions[candidate["name"]], start=1):
                        st.write(f"**{i}.** {question}")

                    st.divider()
                    
                    st.markdown("## 📅 Schedule Interview")
                    #date picker
                    interview_date = st.date_input(
                        "Interview Date",
                        key=f"date_{candidate['name']}"
                    )
                    #time picker
                    interview_time = st.time_input(
                        "Interview Time",
                        key=f"time_{candidate['name']}"
                    )
                    interview_mode = st.selectbox(
                        "Interview Mode",
                        ["Online", "Offline"],
                        key=f"mode_{candidate['name']}"
                    )
                    if st.button("📅 Schedule Interview",key=f"schedule_{candidate['name']}"):
                        already_scheduled = any(
                            interview["candidate"] == candidate["name"]
                            for interview in st.session_state.scheduled_interviews
                        )

                        if already_scheduled:
                            st.warning("⚠️ Interview already scheduled for this candidate.")
                        else:
                            st.session_state.scheduled_interviews.append({

                                "candidate": candidate["name"],

                                "date": interview_date,

                                "time": interview_time,

                                "mode": interview_mode,

                                "status": "Scheduled",

                                "questions": st.session_state.generated_questions[
                                    candidate["name"]
                                ]
                            })
                            st.success("✅ Interview Scheduled Successfully!")
                st.divider()
                        
            st.header("📅 Scheduled Interviews")
            if st.session_state.scheduled_interviews:

                    for interview in st.session_state.scheduled_interviews:

                        with st.container(border=True):

                            st.subheader(f"Interview Scheduled for {interview['candidate']}")

                            st.write(f"📅 Date: {interview['date']}")
                            st.write(f"🕒 Time: {interview['time']}")
                            st.write(f"💻 Mode: {interview['mode']}")
                            st.write(f"📌 Status: {interview['status']}")
     
                        st.divider()
            # ===========================
            # Bottom Candidates
            # ===========================

            st.header("❌ Not Shortlisted Candidates")

            for candidate in bottom_candidates:

                st.subheader(candidate["name"])

                st.progress(candidate["score"] / 100)

                st.write(f"### ⭐ Match Score: {candidate['score']}%")

                st.write(candidate["details"])

                st.divider()