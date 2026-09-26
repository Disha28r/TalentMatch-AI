import os
import json
import tempfile
import uuid
import requests
from pathlib import Path
import pandas as pd

import streamlit as st
from email_service import send_interview_email

from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

from resume_parser import (
    parse_job_description,
    read_resume,
    parse_resume,
    final_score,
     generate_interview_questions,
     analyze_skill_gap
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

                    candidate_id = str(uuid.uuid4())

                    results.append({
                        "candidate_id": candidate_id,
                        "name": parsed_resume.name,
                        "score": result.score,
                        "details": result.details,
                        "resume": parsed_resume
                    })

                    candidate_data = {
                        "candidate_id": candidate_id,
                        "name": parsed_resume.name,
                        "resume_score": result.score,
                        "resume_details": json.dumps(result.details),
                        "matched_skills": [],
                        "missing_required_skills": [],
                        "missing_preferred_skills": [],
                        "partially_matched_skills": [],
                        "skill_gap_summary": "",
                        "recommendations": [],
                        "selection_status": "Pending"
                    }

                    response = requests.post(
                        f"{API_BASE_URL}/candidates",
                        json=candidate_data
                    )

                    if response.status_code != 200:
                        st.error(
                            f"Failed to save candidate {parsed_resume.name}: "
                            f"{response.text}"
                        )

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
            bottom_candidates = results[2:]

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
                if st.button(
                    "🔍 Analyze Skill Gap",
                    key=f"skill_gap_{candidate['name']}"
                ):
                    with st.spinner("Analyzing skill gap..."):

                        skill_gap = analyze_skill_gap(
                            st.session_state.job,
                            candidate["resume"]
                        )
                        skill_gap_data = {
                            "matched_skills": skill_gap.matched_skills,
                            "missing_required_skills": skill_gap.missing_required_skills,
                            "missing_preferred_skills": skill_gap.missing_preferred_skills,
                            "partially_matched_skills": skill_gap.partially_matched_skills,
                            "skill_gap_summary": skill_gap.skill_gap_summary,
                            "recommendations": skill_gap.recommendations
                        }

                        response = requests.put(
                           f"{API_BASE_URL}/candidates/{candidate['candidate_id']}/skill-gap",
                            json=skill_gap_data
                        )

                        if response.status_code == 200:
                            st.success("✅ Skill gap saved successfully!")
                        else:
                            st.error(
                                f"Failed to save skill gap: {response.text}"
                            )

                        st.markdown("### 🔍 Skill Gap Analysis")

                        st.markdown("#### ✅ Matched Skills")

                        for skill in skill_gap.matched_skills:
                            st.write(f"• {skill}")

                        st.markdown("#### ⚠️ Missing Required Skills")

                        for skill in skill_gap.missing_required_skills:
                            st.write(f"• {skill}")

                        st.markdown("#### ⭐ Missing Preferred Skills")

                        for skill in skill_gap.missing_preferred_skills:
                            st.write(f"• {skill}")

                        st.markdown("#### 🟡 Partially Matched Skills")

                        for skill in skill_gap.partially_matched_skills:
                            st.write(f"• {skill}")

                        st.markdown("#### 📝 Skill Gap Summary")

                        st.write(skill_gap.skill_gap_summary)

                        st.markdown("#### 📚 Recommendations")

                        for recommendation in skill_gap.recommendations:
                            st.write(f"• {recommendation}")
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
                            interview_id = str(uuid.uuid4())

                            interview_data = {

                                "interview_id": interview_id,

                                "candidate": candidate["name"],

                                "date": str(interview_date),

                                "time": str(interview_time),

                                "mode": interview_mode,

                                "status": "Scheduled",

                                "questions": st.session_state.generated_questions[
                                    candidate["name"]
                                ]
                            }

                            response = requests.post(
                                f"{API_BASE_URL}/interviews",
                                json={
                                    "interview_id": interview_data["interview_id"],
                                    "candidate": interview_data["candidate"],
                                    "date": interview_data["date"],
                                    "time": interview_data["time"],
                                    "mode": interview_data["mode"],
                                    "questions": interview_data["questions"]
                                }
                            )

                            if response.status_code == 200:

                                st.session_state.scheduled_interviews.append(interview_data)
                                st.success("✅ Interview Scheduled Successfully!")

                            else:

                                st.error("❌ Failed to save interview to database.")
                                st.write(response.text)
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
                            
                            
                            
                            # --------------------------
                            # Join Interview Link
                            # --------------------------

                            candidate_portal_url = os.getenv(
                                "CANDIDATE_PORTAL_URL",
                                "http://localhost:8502"
                            )

                            interview_link = (
                                f"{candidate_portal_url}/?interview_id="
                                f"{interview['interview_id']}"
                            )

                            
                            
                            receiver_email = st.text_input(
                                "Candidate Email",
                                key=f"email_{interview['candidate']}"
                            )

                            if st.button(
                                "📧 Send Invitation",
                                key=f"send_{interview['candidate']}"
                            ):

                                result = send_interview_email(

                                    receiver_email,

                                    interview["candidate"],

                                    interview["date"],

                                    interview["time"],

                                    interview["mode"],
                                    interview_link

                                )

                                if result is True:
                                    st.success("✅ Invitation Sent Successfully!")

                                else:
                                    st.error(result)
     
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
                
                
st.divider()

st.header("📊 Recruiter Dashboard")

response = requests.get(
    f"{API_BASE_URL}/candidates"
)

if response.status_code == 200:

    candidates = response.json()

    if candidates:

        search_name = st.text_input(
            "🔎 Search candidate",
            placeholder="Enter candidate name..."
        )

        min_score = st.slider(
            "🎯 Minimum resume score",
            min_value=0,
            max_value=100,
            value=0
        )
        status_filter = st.selectbox(
            "📌 Selection Status",
            ["All", "Pending", "Selected", "Rejected"]
        )

        filtered_candidates = [
            candidate
            for candidate in candidates
            if search_name.lower() in candidate["name"].lower()
            and (candidate["resume_score"] or 0) >= min_score
            and (
                status_filter == "All"
                or candidate["selection_status"] == status_filter
            )
        ]

        st.subheader(
            f"Candidates ({len(filtered_candidates)})"
        )
        export_data = []

        for candidate in filtered_candidates:
            export_data.append({
                "Candidate": candidate["name"],
                "Resume Score": candidate["resume_score"],
                "Selection Status": candidate["selection_status"],
                "Matched Skills": ", ".join(candidate["matched_skills"]),
                "Missing Required Skills": ", ".join(
                    candidate["missing_required_skills"]
                ),
                "Missing Preferred Skills": ", ".join(
                    candidate["missing_preferred_skills"]
                ),
                "Partially Matched Skills": ", ".join(
                    candidate["partially_matched_skills"]
                ),
                "Skill Gap Summary": candidate["skill_gap_summary"],
                "Recommendations": ", ".join(
                    candidate["recommendations"]
                )
            })

        export_df = pd.DataFrame(export_data)

        csv_data = export_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Candidate Report",
            data=csv_data,
            file_name="talentmatch_candidates.csv",
            mime="text/csv"
        )

        for candidate in filtered_candidates:

            with st.expander(
                f"👤 {candidate['name']} — "
                f"Resume Score: {candidate['resume_score']}"
            ):

                st.write(
                    f"**Selection Status:** "
                    f"{candidate['selection_status']}"
                )

                st.subheader("✅ Matched Skills")

                if candidate["matched_skills"]:
                    for skill in candidate["matched_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No matched skills recorded.")

                st.subheader("❌ Missing Required Skills")

                if candidate["missing_required_skills"]:
                    for skill in candidate["missing_required_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No missing required skills recorded.")

                st.subheader("⭐ Missing Preferred Skills")

                if candidate["missing_preferred_skills"]:
                    for skill in candidate["missing_preferred_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No missing preferred skills recorded.")

                st.subheader("🟡 Partially Matched Skills")

                if candidate["partially_matched_skills"]:
                    for skill in candidate["partially_matched_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No partially matched skills recorded.")

                st.subheader("🧠 Skill Gap Summary")

                if candidate["skill_gap_summary"]:
                    st.write(candidate["skill_gap_summary"])
                else:
                    st.write("Skill gap analysis not available.")

                st.subheader("💡 Recommendations")

                if candidate["recommendations"]:
                    for recommendation in candidate["recommendations"]:
                        st.write(f"• {recommendation}")
                else:
                    st.write("No recommendations recorded.")

    else:
        st.info("No candidates found.")

else:
    st.error("Failed to load candidates.")