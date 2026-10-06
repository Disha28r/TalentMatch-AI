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
    page_title="TalentMatch AI | Recruiter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===========================
# TalentMatch AI Theme
# ===========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: #f7f9fc;
}

/* Hide Streamlit default menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Header */
.talent-header {
    padding: 2rem 0 1.5rem 0;
}

.brand {
    font-size: 2.2rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.25rem;
}

.brand span {
    color: #4f46e5;
}

.tagline {
    font-size: 1.35rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.35rem;
}

.subtitle {
    font-size: 0.95rem;
    color: #6b7280;
}

/* Cards */
.tm-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
}

/* Section headings */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.8rem;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.18);
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    color: white;
}

/* Text area */
.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid #d1d5db;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 12px;
}

/* Divider */
hr {
    border-color: #e5e7eb;
}

/* ===========================
   Candidate Ranking
   =========================== */

.results-header {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}

.candidate-card {
    display: flex;
    align-items: center;
    gap: 1rem;

    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;

    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;

    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

.candidate-rank {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background: #eef2ff;
    color: #4f46e5;

    font-weight: 800;
}

.candidate-info {
    flex: 1;
}

.candidate-name {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
}

.candidate-label {
    font-size: 0.8rem;
    color: #6b7280;
    margin-top: 0.2rem;
}

.candidate-score {
    text-align: right;
    min-width: 120px;
}

.score-value {
    font-size: 1.35rem;
    font-weight: 800;
    color: #111827;
}

.score-strong,
.score-good,
.score-low {
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.15rem;
}

.score-strong {
    color: #059669;
}

.score-good {
    color: #d97706;
}

.score-low {
    color: #dc2626;
}

/* ===========================
   Top Candidate Cards
   =========================== */

.top-candidate-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

.top-badge {
    display: inline-block;
    background: #eef2ff;
    color: #4f46e5;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

.top-name {
    font-size: 1.35rem;
    font-weight: 750;
    color: #111827;
}

.top-score {
    font-size: 2rem;
    font-weight: 800;
    color: #4f46e5;
    margin-top: 0.4rem;
}

.top-score-label {
    font-size: 0.8rem;
    color: #6b7280;
}

.detail-box {
    background: #f8fafc;
    border-radius: 12px;
    padding: 0.9rem;
    margin-top: 1rem;
    color: #4b5563;
    font-size: 0.9rem;
}

/* Candidate action buttons */

.candidate-action-row {
    margin-top: 0.5rem;
}

.stButton > button {
    min-height: 42px;
}
/* ===========================
   Skill Gap UI
   =========================== */

.skill-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.2rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.skill-section-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #374151;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.skill-chip {
    display: inline-block;
    padding: 0.4rem 0.75rem;
    margin: 0.25rem 0.2rem 0.25rem 0;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
}

.skill-matched {
    background: #ecfdf5;
    color: #047857;
}

.skill-required {
    background: #fef2f2;
    color: #b91c1c;
}

.skill-preferred {
    background: #fffbeb;
    color: #b45309;
}

.skill-partial {
    background: #eff6ff;
    color: #1d4ed8;
}

.skill-summary {
    background: #f8fafc;
    border-left: 4px solid #4f46e5;
    border-radius: 10px;
    padding: 1rem;
    color: #4b5563;
    line-height: 1.6;
}

.recommendation-item {
    background: #f8fafc;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
    color: #374151;
}

/* ===========================
   Interview Questions UI
   =========================== */

.interview-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.3rem;
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.interview-question {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
}

.question-number {
    min-width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 0.8rem;
    font-weight: 800;
}

.question-text {
    color: #1f2937;
    font-size: 0.92rem;
    line-height: 1.55;
    padding-top: 0.25rem;
}

.interview-header {
    margin-bottom: 1rem;
}

.interview-title {
    font-size: 1.15rem;
    font-weight: 750;
    color: #111827;
}

.interview-subtitle {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 0.25rem;
}

/* ===========================
   Interview Scheduling UI
   =========================== */

.schedule-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.3rem;
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.schedule-header {
    margin-bottom: 1rem;
}

.schedule-title {
    font-size: 1.15rem;
    font-weight: 750;
    color: #111827;
}

.schedule-subtitle {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 0.25rem;
}

.schedule-success {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    color: #047857;
    font-weight: 600;
    margin-top: 1rem;
}

/* ===========================
   Scheduled Interviews UI
   =========================== */

.scheduled-section {
    margin-top: 2rem;
    margin-bottom: 1.5rem;
}

.scheduled-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.scheduled-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.scheduled-candidate-name {
    font-size: 1.05rem;
    font-weight: 750;
    color: #111827;
}

.scheduled-status {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: #ecfdf5;
    color: #047857;
    font-size: 0.75rem;
    font-weight: 700;
}

.interview-detail {
    background: #f8fafc;
    border-radius: 12px;
    padding: 0.75rem 0.9rem;
    margin-bottom: 0.7rem;
}

.interview-detail-label {
    font-size: 0.72rem;
    color: #6b7280;
    margin-bottom: 0.2rem;
}

.interview-detail-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: #1f2937;
}

.interview-link-box {
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    border-radius: 12px;
    padding: 0.9rem;
    margin-top: 1rem;
}

.interview-link-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #4338ca;
    margin-bottom: 0.35rem;
}

.interview-link {
    font-size: 0.82rem;
    color: #4f46e5;
    word-break: break-all;
}

/* ===========================
   Not Shortlisted Candidates
   =========================== */

.not-shortlisted-section {
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.not-shortlisted-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.03);
}

.not-shortlisted-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.not-shortlisted-name {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
}

.not-shortlisted-score {
    font-size: 1rem;
    font-weight: 800;
    color: #dc2626;
}

.not-shortlisted-label {
    font-size: 0.78rem;
    color: #9ca3af;
    margin-top: 0.2rem;
}

.not-shortlisted-details {
    background: #f8fafc;
    border-radius: 10px;
    padding: 0.8rem;
    margin-top: 0.9rem;
    color: #4b5563;
    font-size: 0.88rem;
    line-height: 1.5;
}

/* ===========================
   Main Navigation
   =========================== */

.main-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 0.45rem;
    margin: 0.5rem 0 2rem 0;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

.nav-brand {
    font-size: 0.95rem;
    font-weight: 700;
    color: #111827;
    padding-left: 0.8rem;
}

.nav-brand span {
    color: #4f46e5;
}

.nav-item {
    padding: 0.55rem 1.1rem;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
}

.nav-active {
    background: #eef2ff;
    color: #4f46e5;
}

.nav-inactive {
    color: #6b7280;
}

/* ===========================
   Dashboard Metrics
   =========================== */

.dashboard-metrics {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    flex: 1;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.2rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.metric-label {
    font-size: 0.78rem;
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 0.45rem;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #111827;
}

.metric-description {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.25rem;
}

/* ===========================
   Dashboard Filters
   =========================== */

.dashboard-filter-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.dashboard-filter-title {
    font-size: 1rem;
    font-weight: 750;
    color: #111827;
    margin-bottom: 0.2rem;
}

.dashboard-filter-subtitle {
    font-size: 0.8rem;
    color: #6b7280;
    margin-bottom: 1rem;
}

.dashboard-results-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1.4rem;
    margin-bottom: 1rem;
}

.dashboard-results-title {
    font-size: 1.05rem;
    font-weight: 750;
    color: #111827;
}

.dashboard-results-count {
    background: #eef2ff;
    color: #4f46e5;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* ===========================
   Dashboard Candidate Cards
   =========================== */

.dashboard-candidate-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.dashboard-candidate-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.dashboard-candidate-name {
    font-size: 1.05rem;
    font-weight: 750;
    color: #111827;
}

.dashboard-candidate-status {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: #f3f4f6;
    color: #4b5563;
    font-size: 0.72rem;
    font-weight: 700;
}

.dashboard-score {
    font-size: 1.35rem;
    font-weight: 800;
    color: #4f46e5;
}

.dashboard-score-label {
    font-size: 0.7rem;
    color: #9ca3af;
    text-align: right;
}

.dashboard-skill-group {
    margin-top: 1rem;
}

.dashboard-skill-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: #6b7280;
    margin-bottom: 0.45rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.dashboard-skill-list {
    color: #374151;
    font-size: 0.85rem;
    line-height: 1.6;
}

.dashboard-recommendation {
    background: #f8fafc;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-top: 1rem;
    color: #4b5563;
    font-size: 0.85rem;
}

.dashboard-skill-warning {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-top: 0.8rem;
    color: #9a3412;
    font-size: 0.85rem;
}

.dashboard-skill-partial {
    background: #fefce8;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-top: 0.8rem;
    color: #854d0e;
    font-size: 0.85rem;
}

.dashboard-gap-summary {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-top: 0.8rem;
    color: #4b5563;
    font-size: 0.85rem;
    line-height: 1.5;
}

/* ===========================
   Dashboard Skill Chips
   =========================== */

.skill-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
}

.skill-chip {
    display: inline-block;
    padding: 0.35rem 0.65rem;
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    border-radius: 999px;
    color: #4338ca;
    font-size: 0.75rem;
    font-weight: 650;
}

.skill-chip-missing {
    display: inline-block;
    padding: 0.35rem 0.65rem;
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 999px;
    color: #c2410c;
    font-size: 0.75rem;
    font-weight: 650;
}

.skill-chip-partial {
    display: inline-block;
    padding: 0.35rem 0.65rem;
    background: #fefce8;
    border: 1px solid #fde68a;
    border-radius: 999px;
    color: #a16207;
    font-size: 0.75rem;
    font-weight: 650;
}

/* ===========================
   Hiring Pipeline
   =========================== */

.pipeline-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1.25rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.pipeline-title {
    font-size: 1.05rem;
    font-weight: 750;
    color: #111827;
    margin-bottom: 0.25rem;
}

.pipeline-subtitle {
    font-size: 0.8rem;
    color: #6b7280;
    margin-bottom: 1.2rem;
}

.pipeline-row {
    margin-bottom: 1rem;
}

.pipeline-row-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}

.pipeline-label {
    font-size: 0.82rem;
    font-weight: 650;
    color: #374151;
}

.pipeline-count {
    font-size: 0.8rem;
    font-weight: 750;
    color: #4f46e5;
}

.pipeline-bar {
    width: 100%;
    height: 9px;
    background: #eef2f7;
    border-radius: 999px;
    overflow: hidden;
}

.pipeline-fill {
    height: 100%;
    background: #6366f1;
    border-radius: 999px;
}
</style>
""", unsafe_allow_html=True)

# ===========================
# Recruiter Dashboard Page
# ===========================

def render_recruiter_dashboard():

    st.html("""
    <div class="results-header">
        <div>
            <div class="section-title">
                📊 Recruiter Dashboard
            </div>

            <div class="subtitle">
                Overview of candidates, scores, interviews and hiring activity.
            </div>
        </div>
    </div>
    """)

    response = requests.get(
        f"{API_BASE_URL}/candidates"
    )

    if response.status_code == 200:

        candidates = response.json()

        # ===========================
        # Dashboard Metrics
        # ===========================

        total_candidates = len(candidates)

        scores = [
            candidate["resume_score"]
            for candidate in candidates
            if candidate.get("resume_score") is not None
        ]

        average_score = (
            round(sum(scores) / len(scores))
            if scores
            else 0
        )

        selected_candidates = sum(
            1
            for candidate in candidates
            if candidate.get("selection_status") == "Selected"
        )

        scheduled_interviews = len(
            st.session_state.scheduled_interviews
        )
        
        pending_candidates = sum(
            1
            for candidate in candidates
            if candidate.get("selection_status") == "Pending"
        )

        rejected_candidates = sum(
            1
            for candidate in candidates
            if candidate.get("selection_status") == "Rejected"
        )

        total_for_pipeline = len(candidates)

        st.html(f"""
        <div class="dashboard-metrics">

            <div class="metric-card">
                <div class="metric-label">
                    TOTAL CANDIDATES
                </div>

                <div class="metric-value">
                    {total_candidates}
                </div>

                <div class="metric-description">
                    Candidates analyzed
                </div>
            </div>


            <div class="metric-card">
                <div class="metric-label">
                    AVERAGE SCORE
                </div>

                <div class="metric-value">
                    {average_score}%
                </div>

                <div class="metric-description">
                    Resume match score
                </div>
            </div>


            <div class="metric-card">
                <div class="metric-label">
                    INTERVIEWS
                </div>

                <div class="metric-value">
                    {scheduled_interviews}
                </div>

                <div class="metric-description">
                    Interviews scheduled
                </div>
            </div>


            <div class="metric-card">
                <div class="metric-label">
                    SELECTED
                </div>

                <div class="metric-value">
                    {selected_candidates}
                </div>

                <div class="metric-description">
                    Selected candidates
                </div>
            </div>

        </div>
        """)
        
        st.html(f"""
        <div class="pipeline-section">

            <div class="pipeline-title">
                Hiring Pipeline
            </div>

            <div class="pipeline-subtitle">
                Current distribution of candidates across the hiring process.
            </div>


            <div class="pipeline-row">

                <div class="pipeline-row-header">

                    <div class="pipeline-label">
                        Pending
                    </div>

                    <div class="pipeline-count">
                        {pending_candidates}
                    </div>

                </div>

                <div class="pipeline-bar">

                    <div
                        class="pipeline-fill"
                        style="width: {
                            (pending_candidates / total_for_pipeline * 100)
                            if total_for_pipeline else 0
                        }%;"
                    ></div>

                </div>

            </div>


            <div class="pipeline-row">

                <div class="pipeline-row-header">

                    <div class="pipeline-label">
                        Selected
                    </div>

                    <div class="pipeline-count">
                        {selected_candidates}
                    </div>

                </div>

                <div class="pipeline-bar">

                    <div
                        class="pipeline-fill"
                        style="width: {
                            (selected_candidates / total_for_pipeline * 100)
                            if total_for_pipeline else 0
                        }%;"
                    ></div>

                </div>

            </div>


            <div class="pipeline-row">

                <div class="pipeline-row-header">

                    <div class="pipeline-label">
                        Rejected
                    </div>

                    <div class="pipeline-count">
                        {rejected_candidates}
                    </div>

                </div>

                <div class="pipeline-bar">

                    <div
                        class="pipeline-fill"
                        style="width: {
                            (rejected_candidates / total_for_pipeline * 100)
                            if total_for_pipeline else 0
                        }%;"
                    ></div>

                </div>

            </div>

        </div>
        """)

        if candidates:

            st.html("""
                        <div class="dashboard-filter-card">

                            <div class="dashboard-filter-title">
                                🔎 Candidate Filters
                            </div>

                            <div class="dashboard-filter-subtitle">
                                Search and filter candidates by name, resume score and hiring status.
                            </div>

                        </div>
                        """)

            filter_col1, filter_col2, filter_col3 = st.columns(
                            [2, 1, 1],
                            gap="medium"
                        )

            with filter_col1:

                search_name = st.text_input(
                    "Search candidate",
                    placeholder="Enter candidate name...",
                    label_visibility="collapsed"
                )

            with filter_col2:

                min_score = st.slider(
                    "Minimum score",
                    min_value=0,
                    max_value=100,
                    value=0
                )

            with filter_col3:

                status_filter = st.selectbox(
                    "Selection Status",
                    ["All", "Pending", "Selected", "Rejected"],
                    label_visibility="collapsed"
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

            st.html(f"""
            <div class="dashboard-results-header">

                <div class="dashboard-results-title">
                    Candidate Results
                </div>

                <div class="dashboard-results-count">
                    {len(filtered_candidates)} candidates
                </div>

            </div>
            """)

            export_data = []

            for candidate in filtered_candidates:

                export_data.append({
                    "Candidate": candidate["name"],
                    "Resume Score": candidate["resume_score"],
                    "Selection Status": candidate["selection_status"],
                    "Matched Skills": ", ".join(
                        candidate["matched_skills"]
                    ),
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

                matched_skills = candidate.get(
                    "matched_skills", []
                )
                
                missing_preferred = candidate.get(
                    "missing_preferred_skills", []
                )

                partially_matched = candidate.get(
                    "partially_matched_skills", []
                )

                skill_gap_summary = candidate.get(
                    "skill_gap_summary",
                    ""
                )

                missing_required = candidate.get(
                    "missing_required_skills", []
                )

                recommendations = candidate.get(
                    "recommendations", []
                )

                selection_status = candidate.get(
                    "selection_status",
                    "Pending"
                )

                resume_score = candidate.get(
                    "resume_score",
                    0
                )

                matched_chips = ""

                for skill in matched_skills:
                    matched_chips += f"""
                    <span class="skill-chip">
                        {skill}
                    </span>
                    """

                if not matched_chips:
                    matched_chips = """
                    <span style="color:#9ca3af; font-size:0.85rem;">
                        No matched skills recorded.
                    </span>
                    """
                    
                missing_chips = ""

                for skill in missing_required:
                    missing_chips += f"""
                    <span class="skill-chip-missing">
                        {skill}
                    </span>
                    """

                if not missing_chips:
                    missing_chips = """
                    <span style="color:#9ca3af; font-size:0.85rem;">
                        No missing required skills.
                    </span>
                    """
                    
                partial_chips = ""

                for skill in partially_matched:
                    partial_chips += f"""
                    <span class="skill-chip-partial">
                        {skill}
                    </span>
                    """

                if not partial_chips:
                    partial_chips = """
                    <span style="color:#9ca3af; font-size:0.85rem;">
                        No partially matched skills.
                    </span>
                    """

                missing_text = (
                    ", ".join(missing_required)
                    if missing_required
                    else "No missing required skills."
                )

                recommendation_text = (
                    " • ".join(recommendations)
                    if recommendations
                    else "No recommendations recorded."
                )

                st.html(f"""
                <div class="dashboard-candidate-card">

                    <div class="dashboard-candidate-header">

                        <div>
                            <div class="dashboard-candidate-name">
                                👤 {candidate["name"]}
                            </div>

                            <div class="dashboard-candidate-status">
                                {selection_status}
                            </div>
                        </div>

                        <div>
                            <div class="dashboard-score">
                                {resume_score}%
                            </div>

                            <div class="dashboard-score-label">
                                RESUME MATCH
                            </div>
                        </div>

                    </div>


                    <div class="dashboard-skill-group">

                        <div class="dashboard-skill-title">
                            Matched Skills
                        </div>

                        <div class="skill-chips">
                            {matched_chips}
                        </div>

                    </div>


                    <div class="dashboard-skill-group">

                        <div class="dashboard-skill-title">
                            Missing Required Skills
                        </div>

                        <div class="skill-chips">
                            {missing_chips}
                        </div>

                    </div>
                    
                    <div class="dashboard-skill-group">

                    <div class="dashboard-skill-title">
                        Missing Preferred Skills
                    </div>

                    <div class="dashboard-skill-list">
                        {", ".join(missing_preferred)
                        if missing_preferred
                        else "No missing preferred skills."}
                    </div>

                </div>


                <div class="dashboard-skill-group">

                    <div class="dashboard-skill-title">
                        Partially Matched Skills
                    </div>

                    <div class="skill-chips">
                        {partial_chips}
                    </div>

                </div>


                <div class="dashboard-gap-summary">

                    <strong>🧠 Skill Gap Summary</strong>

                    <br>

                    {skill_gap_summary
                    if skill_gap_summary
                    else "Skill gap analysis not available."}

                </div>


                    <div class="dashboard-recommendation">

                        <strong>💡 Recommendation</strong>

                        <br>

                        {recommendation_text}

                    </div>

                </div>
                """)
                
                status_col1, status_col2, status_col3 = st.columns(
                    [1, 1, 3],
                    gap="small"
                )

                with status_col1:

                    if st.button(
                        "✓ Select",
                        key=f"select_{candidate['candidate_id']}",
                        use_container_width=True
                    ):

                        response = requests.put(
                            f"{API_BASE_URL}/candidates/"
                            f"{candidate['candidate_id']}/status",
                            params={
                                "status": "Selected"
                            }
                        )

                        if response.status_code == 200:
                            st.success(
                                "Candidate selected successfully."
                            )
                            st.rerun()
                        else:
                            st.error(
                                "Failed to update candidate status."
                            )

                with status_col2:

                    if st.button(
                        "✕ Reject",
                        key=f"reject_{candidate['candidate_id']}",
                        use_container_width=True
                    ):

                        response = requests.put(
                            f"{API_BASE_URL}/candidates/"
                            f"{candidate['candidate_id']}/status",
                            params={
                                "status": "Rejected"
                            }
                        )

                        if response.status_code == 200:
                            st.success(
                                "Candidate rejected."
                            )
                            st.rerun()
                        else:
                            st.error(
                                "Failed to update candidate status."
                            )

        else:
            st.info("No candidates found.")

    else:
        st.error("Failed to load candidates.")
    


# ===========================
# TalentMatch AI Header
# ===========================
st.html("""
<div class="talent-header">

    <div class="brand">
        🎯 Talent<span>Match AI</span>
    </div>

    <div class="tagline">
        Find the right talent. Faster.
    </div>

    <div class="subtitle">
        AI-powered recruitment from resume screening to interview evaluation.
    </div>

</div>
""")

# ===========================
# Main Navigation
# ===========================

page = st.radio(
    "Navigation",
    [
        "👤 Candidate Analysis",
        "📊 Recruiter Dashboard"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

# ===========================
# Page Selection
# ===========================

if page == "📊 Recruiter Dashboard":

    render_recruiter_dashboard()

    st.stop()
# ---------------- New Analysis ----------------

if st.button("🔄 New Analysis"):
    st.session_state.analysis_done = False
    st.session_state.results = []
    st.session_state.job = None
    st.rerun()

# ===========================
# Hiring Inputs
# ===========================

st.markdown("""
<div class="section-title">
    Start a New Hiring Search
</div>

<div class="subtitle" style="margin-bottom: 1.2rem;">
    Add the role requirements and candidate resumes to let TalentMatch AI
    identify the strongest matches.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

# ---------------------------
# Job Description
# ---------------------------

with col1:

    st.html("""
            <div class="tm-card">
                <div class="section-title">
                    📋 Job Description
                </div>

                <div class="subtitle">
                    Paste the job description for the role you're hiring for.
                </div>
            </div>
            """)

    job_description = st.text_area(
        "Job Description",
        height=250,
        placeholder="""Example:

We are looking for a Python Developer with experience in
FastAPI, PostgreSQL, REST APIs and cloud deployment...

Paste the complete job description here.""",
        label_visibility="collapsed"
    )


# ---------------------------
# Candidate Resumes
# ---------------------------

with col2:

    st.html("""
        <div class="tm-card">
            <div class="section-title">
                📄 Candidate Resumes
            </div>

            <div class="subtitle">
                Upload candidate resumes in PDF or DOCX format.
            </div>
        </div>
        """)

    uploaded_resumes = st.file_uploader(
        "Candidate Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_resumes:
        st.success(
            f"✓ {len(uploaded_resumes)} resume(s) ready for analysis"
        )


# ===========================
# Analyze Button
# ===========================

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

analyze_clicked = st.button(
    "✨ Analyze Candidates",
    type="primary",
    use_container_width=True
)

# ---------------- Analyze ----------------

if analyze_clicked:

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

            # ===========================
            # Candidate Rankings
            # ===========================

            st.html("""
            <div class="results-header">
                <div>
                    <div class="section-title">Candidate Rankings</div>
                    <div class="subtitle">
                        AI-powered ranking based on job description and resume match.
                    </div>
                </div>
            </div>
            """)

            for rank, candidate in enumerate(results, start=1):

                score = candidate["score"]

                if score >= 85:
                    score_label = "Strong Match"
                    score_class = "score-strong"
                elif score >= 70:
                    score_label = "Good Match"
                    score_class = "score-good"
                else:
                    score_label = "Low Match"
                    score_class = "score-low"

                st.html(f"""
                <div class="candidate-card">

                    <div class="candidate-rank">
                        #{rank}
                    </div>

                    <div class="candidate-info">
                        <div class="candidate-name">
                            {candidate["name"]}
                        </div>

                        <div class="candidate-label">
                            Candidate Profile
                        </div>
                    </div>

                    <div class="candidate-score">
                        <div class="score-value">
                            {score}%
                        </div>

                        <div class="{score_class}">
                            {score_label}
                        </div>
                    </div>

                </div>
                """)
        
        
            # scheduled_interviews = []

            # ===========================
            # Top Candidates
            # ===========================

            st.html("""
            <div class="results-header">
                <div class="section-title">🏆 Top Candidates</div>
                <div class="subtitle">
                    The strongest matches identified by TalentMatch AI.
                </div>
            </div>
            """)

            for index, candidate in enumerate(top_candidates):

                if index == 0:
                    badge = "🥇 TOP MATCH"
                else:
                    badge = "🥈 SECOND BEST"

                score = candidate["score"]

                st.html(f"""
                <div class="top-candidate-card">

                    <div class="top-badge">
                        {badge}
                    </div>

                    <div class="top-name">
                        {candidate["name"]}
                    </div>

                    <div class="top-score">
                        {score}%
                    </div>

                    <div class="top-score-label">
                        Resume Match Score
                    </div>

                    <div class="detail-box">
                        {candidate["details"]}
                    </div>

                </div>
                """)

                # Candidate actions
                action_col1, action_col2 = st.columns(2)

                with action_col1:

                    skill_gap_clicked = st.button(
                        "🔍 Analyze Skill Gap",
                        key=f"skill_gap_{candidate['candidate_id']}",
                        use_container_width=True
                    )

                with action_col2:

                    interview_questions_clicked = st.button(
                        "🎤 Generate Interview Questions",
                        key=f"generate_{candidate['candidate_id']}",
                        use_container_width=True
                    )

               # ---------------------------
                # Skill Gap Analysis
                # ---------------------------

                if skill_gap_clicked:

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

                        # ---------------------------
                        # Skill Gap Results
                        # ---------------------------

                        # ---------------------------
                    # Skill Gap UI
                    # ---------------------------

                    st.html("""
                    <div class="results-header">
                        <div class="section-title">🔍 Skill Gap Analysis</div>
                        <div class="subtitle">
                            Understand where the candidate matches the role and where development is needed.
                        </div>
                    </div>
                    """)


                    # ---------------------------
                    # Matched Skills
                    # ---------------------------

                    matched_html = ""

                    for skill in skill_gap.matched_skills:
                        matched_html += f"""
                        <span class="skill-chip skill-matched">
                            ✓ {skill}
                        </span>
                        """

                    if not matched_html:
                        matched_html = "<span>No matched skills identified.</span>"


                    st.html(f"""
                    <div class="skill-section">

                        <div class="skill-section-title">
                            ✅ Matched Skills
                        </div>

                        {matched_html}

                    </div>
                    """)


                    # ---------------------------
                    # Required + Preferred Gaps
                    # ---------------------------

                    required_html = ""

                    for skill in skill_gap.missing_required_skills:
                        required_html += f"""
                        <span class="skill-chip skill-required">
                            {skill}
                        </span>
                        """

                    if not required_html:
                        required_html = "<span>No missing required skills.</span>"


                    preferred_html = ""

                    for skill in skill_gap.missing_preferred_skills:
                        preferred_html += f"""
                        <span class="skill-chip skill-preferred">
                            {skill}
                        </span>
                        """

                    if not preferred_html:
                        preferred_html = "<span>No missing preferred skills.</span>"


                    gap_col1, gap_col2 = st.columns(2, gap="large")


                    with gap_col1:

                        st.html(f"""
                        <div class="skill-section">

                            <div class="skill-section-title">
                                ⚠️ Missing Required Skills
                            </div>

                            {required_html}

                        </div>
                        """)


                    with gap_col2:

                        st.html(f"""
                        <div class="skill-section">

                            <div class="skill-section-title">
                                ⭐ Missing Preferred Skills
                            </div>

                            {preferred_html}

                        </div>
                        """)


                    # ---------------------------
                    # Partially Matched Skills
                    # ---------------------------

                    partial_html = ""

                    for skill in skill_gap.partially_matched_skills:
                        partial_html += f"""
                        <span class="skill-chip skill-partial">
                            {skill}
                        </span>
                        """

                    if not partial_html:
                        partial_html = "<span>No partially matched skills.</span>"


                    st.html(f"""
                    <div class="skill-section">

                        <div class="skill-section-title">
                            🟡 Partially Matched Skills
                        </div>

                        {partial_html}

                    </div>
                    """)


                    # ---------------------------
                    # Summary
                    # ---------------------------

                    st.html(f"""
                    <div class="skill-section">

                        <div class="skill-section-title">
                            📝 AI Skill Gap Summary
                        </div>

                        <div class="skill-summary">
                            {skill_gap.skill_gap_summary}
                        </div>

                    </div>
                    """)


                    # ---------------------------
                    # Recommendations
                    # ---------------------------

                    recommendations_html = ""

                    for recommendation in skill_gap.recommendations:
                        recommendations_html += f"""
                        <div class="recommendation-item">
                            💡 {recommendation}
                        </div>
                        """

                    if not recommendations_html:
                        recommendations_html = """
                        <div class="recommendation-item">
                            No additional recommendations available.
                        </div>
                        """


                    st.html(f"""
                    <div class="skill-section">

                        <div class="skill-section-title">
                            📚 Recommendations
                        </div>

                        {recommendations_html}

                    </div>
                    """)



                # ---------------------------
                # Interview Questions
                # ---------------------------

                if interview_questions_clicked:

                    with st.spinner("Generating interview questions..."):

                        questions = generate_interview_questions(
                            st.session_state.job,
                            candidate["resume"]
                        )

                        # Store questions using candidate_id
                        st.session_state.generated_questions[
                            candidate["candidate_id"]
                        ] = questions.questions


                # ---------------------------
                # Display Interview Questions
                # ---------------------------

                if candidate["candidate_id"] in st.session_state.generated_questions:

                    generated_questions = st.session_state.generated_questions[
                        candidate["candidate_id"]
                    ]

                    st.html("""
                    <div class="interview-section">

                        <div class="interview-header">

                            <div class="interview-title">
                                🎤 AI Interview Questions
                            </div>

                            <div class="interview-subtitle">
                                AI-generated questions tailored to this candidate and role.
                            </div>

                        </div>
                    """)

                    for i, question in enumerate(
                        generated_questions,
                        start=1
                    ):

                        st.html(f"""
                        <div class="interview-question">

                            <div class="question-number">
                                {i:02d}
                            </div>

                            <div class="question-text">
                                {question}
                            </div>

                        </div>
                        """)

                    st.html("""
                    </div>
                    """)


                    # ---------------------------
                    # Schedule Interview
                    # ---------------------------

                    st.html("""
                    <div class="schedule-section">

                        <div class="schedule-header">

                            <div class="schedule-title">
                                📅 Schedule Interview
                            </div>

                            <div class="schedule-subtitle">
                                Choose when and how you want to conduct the candidate interview.
                            </div>

                        </div>

                    </div>
                    """)

                    schedule_col1, schedule_col2, schedule_col3 = st.columns(
                        3,
                        gap="medium"
                    )

                    with schedule_col1:

                        interview_date = st.date_input(
                            "Interview Date",
                            key=f"date_{candidate['candidate_id']}"
                        )

                    with schedule_col2:

                        interview_time = st.time_input(
                            "Interview Time",
                            key=f"time_{candidate['candidate_id']}"
                        )

                    with schedule_col3:

                        interview_mode = st.selectbox(
                            "Interview Mode",
                            ["Online", "Offline"],
                            key=f"mode_{candidate['candidate_id']}"
                        )


                    if st.button(
                        "📅 Schedule Interview",
                        key=f"schedule_{candidate['candidate_id']}",
                        type="primary",
                        use_container_width=True
                    ):

                        already_scheduled = any(
                            interview["candidate_id"] == candidate["candidate_id"]
                            for interview in st.session_state.scheduled_interviews
                        )

                        if already_scheduled:

                            st.warning(
                                "⚠️ Interview already scheduled for this candidate."
                            )

                        else:

                            interview_id = str(uuid.uuid4())

                            interview_data = {

                                "interview_id": interview_id,

                                "candidate_id": candidate["candidate_id"],

                                "candidate": candidate["name"],

                                "date": str(interview_date),

                                "time": str(interview_time),

                                "mode": interview_mode,

                                "status": "Scheduled",

                                "questions": generated_questions
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

                                st.session_state.scheduled_interviews.append(
                                    interview_data
                                )

                                st.html("""
                                <div class="schedule-success">
                                    ✓ Interview Scheduled Successfully!
                                </div>
                                """)

                            else:

                                st.error(
                                    "❌ Failed to save interview to database."
                                )

                                st.write(response.text)

                st.divider()
                        
            # ===========================
            # Scheduled Interviews
            # ===========================

            st.html("""
            <div class="scheduled-section">

                <div class="results-header">

                    <div class="section-title">
                        📅 Scheduled Interviews
                    </div>

                    <div class="subtitle">
                        Manage upcoming candidate interviews and send interview invitations.
                    </div>

                </div>

            </div>
            """)

            if st.session_state.scheduled_interviews:

                for interview in st.session_state.scheduled_interviews:

                    st.html(f"""
                    <div class="scheduled-card">

                        <div class="scheduled-card-header">

                            <div class="scheduled-candidate-name">
                                👤 {interview["candidate"]}
                            </div>

                            <div class="scheduled-status">
                                ✓ {interview["status"]}
                            </div>

                        </div>

                        <div class="interview-detail">
                            <div class="interview-detail-label">
                                DATE
                            </div>

                            <div class="interview-detail-value">
                                📅 {interview["date"]}
                            </div>
                        </div>

                        <div class="interview-detail">
                            <div class="interview-detail-label">
                                TIME
                            </div>

                            <div class="interview-detail-value">
                                🕐 {interview["time"]}
                            </div>
                        </div>

                        <div class="interview-detail">
                            <div class="interview-detail-label">
                                INTERVIEW MODE
                            </div>

                            <div class="interview-detail-value">
                                💻 {interview["mode"]}
                            </div>
                        </div>

                    </div>
                    """)

                    # ---------------------------
                    # Candidate Interview Link
                    # ---------------------------

                    candidate_portal_url = os.getenv(
                        "CANDIDATE_PORTAL_URL",
                        "http://localhost:8502"
                    )

                    interview_link = (
                        f"{candidate_portal_url}/?interview_id="
                        f"{interview['interview_id']}"
                    )

                    st.html(f"""
                    <div class="interview-link-box">

                        <div class="interview-link-label">
                            🔗 CANDIDATE INTERVIEW LINK
                        </div>

                        <div class="interview-link">
                            {interview_link}
                        </div>

                    </div>
                    """)

                    # ---------------------------
                    # Send Invitation
                    # ---------------------------

                    receiver_email = st.text_input(
                        "Candidate Email",
                        key=f"email_{interview['candidate']}",
                        placeholder="Enter candidate email..."
                    )

                    if st.button(
                        "📧 Send Invitation",
                        key=f"send_{interview['candidate']}",
                        type="primary",
                        use_container_width=True
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

                            st.success(
                                "✅ Invitation Sent Successfully!"
                            )

                        else:

                            st.error(result)

                    st.markdown(
                        "<div style='height: 0.5rem;'></div>",
                        unsafe_allow_html=True
                    )

            else:

                st.html("""
                <div class="scheduled-card">

                    <div class="scheduled-candidate-name">
                        No interviews scheduled yet
                    </div>

                    <div class="subtitle">
                        Schedule an interview for a candidate to see it here.
                    </div>

                </div>
                """)
           # ===========================
            # Not Shortlisted Candidates
            # ===========================

            st.html("""
            <div class="not-shortlisted-section">

                <div class="results-header">

                    <div class="section-title">
                        ❌ Other Candidates
                    </div>

                    <div class="subtitle">
                        Candidates with lower resume-match scores for this role.
                    </div>

                </div>

            </div>
            """)

            if bottom_candidates:

                for candidate in bottom_candidates:

                    score = candidate["score"]

                    st.html(f"""
                    <div class="not-shortlisted-card">

                        <div class="not-shortlisted-header">

                            <div>
                                <div class="not-shortlisted-name">
                                    {candidate["name"]}
                                </div>

                                <div class="not-shortlisted-label">
                                    Candidate Profile
                                </div>
                            </div>

                            <div class="not-shortlisted-score">
                                {score}%
                            </div>

                        </div>

                        <div class="not-shortlisted-details">
                            {candidate["details"]}
                        </div>

                    </div>
                    """)

            else:

                st.html("""
                <div class="not-shortlisted-card">

                    <div class="not-shortlisted-name">
                        No additional candidates
                    </div>

                    <div class="not-shortlisted-label">
                        All analyzed candidates are currently displayed in the top matches.
                    </div>

                </div>
                """)
                
                
