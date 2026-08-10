import os
import tempfile
from pathlib import Path

import streamlit as st

from resume_parser import (
    parse_job_description,
    read_resume,
    parse_resume,
    final_score
    #generate_interview_questions
)

# ---------------- Session State ----------------

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
                st.divider()
            # ===========================
            # Bottom Candidates
            # ===========================

            st.header("⚠️ Bottom 2 Candidates")

            for candidate in bottom_candidates:

                st.subheader(candidate["name"])

                st.progress(candidate["score"] / 100)

                st.write(f"### ⭐ Match Score: {candidate['score']}%")

                st.write(candidate["details"])

                st.divider()