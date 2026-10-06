# 🎯 TalentMatch AI

An AI-powered recruitment platform that helps recruiters screen resumes, identify candidate skill gaps, schedule interviews, and evaluate candidate responses.

TalentMatch AI combines AI-powered resume analysis with a recruiter dashboard and candidate interview portal to streamline the recruitment process from resume screening to interview evaluation.

---

## 🚀 Live Demo

### 👩‍💼 Recruiter Portal

https://talentmatch-recruiter.onrender.com/

### 👤 Candidate Portal

https://talentmatch-candidate.onrender.com/

> The Candidate Portal requires a valid interview link containing an `interview_id`.

### ⚙️ Backend API

https://talentmatch-ai-rgky.onrender.com/

### ❤️ API Health Check

https://talentmatch-ai-rgky.onrender.com/health

---

## ✨ Features

### 📄 AI Resume Screening

- Upload a Job Description
- Upload multiple resumes in PDF or DOCX format
- Extract candidate information using AI
- Compare resumes against the Job Description
- Generate candidate match scores
- Rank candidates based on the match score

### 🎯 Skill Gap Analysis

TalentMatch AI identifies:

- ✅ Matched Skills
- ❌ Missing Required Skills
- ⭐ Missing Preferred Skills
- ⚠️ Partially Matched Skills
- 💡 Skill Gap Summary
- 📌 Recommendations

### 📊 Recruiter Dashboard

TalentMatch AI provides a dedicated recruiter dashboard for managing the hiring pipeline.

Recruiters can:

- Search candidates by name
- Filter candidates by resume score
- Filter candidates by selection status
- View candidate match scores
- Review matched and missing skills
- Review skill-gap summaries and recommendations
- Track candidates through Pending, Selected and Rejected stages
- Select or reject candidates directly from the dashboard
- Monitor the hiring pipeline
- Export candidate information as CSV

### 💬 AI-Generated Interview Questions

TalentMatch AI generates interview questions based on the Job Description and candidate profile.

### 📅 Interview Scheduling

Recruiters can schedule interviews with:

- Candidate
- Date
- Time
- Interview Mode
- AI-generated Interview Questions

### 📧 Interview Invitations

The system generates candidate-specific interview links that can be shared with applicants.

### 🎥 Video Interview

Candidates can record video answers directly through the Candidate Portal.

Recorded videos are uploaded to the FastAPI backend and stored as interview recordings.

### 🎙️ Voice Interview & Speech-to-Text

Candidates can record spoken answers.

The recorded audio is transcribed using Groq Speech-to-Text.

The generated transcript is automatically added to the candidate's answer.

### 🤖 AI Interview Evaluation

After completing the interview, TalentMatch AI evaluates the candidate's responses and provides:

- Overall Score
- Technical Knowledge
- Communication
- Problem Solving
- Strengths
- Areas for Improvement
- Recommendation
- Brief Feedback

### 🗄️ PostgreSQL Data Storage

Candidate and interview information is stored in PostgreSQL.

The deployed application uses Neon PostgreSQL.

---

## 🛠️ Tech Stack

### Frontend
- Streamlit
- HTML / CSS
- Browser MediaRecorder API

### Backend
- Python
- FastAPI
- Uvicorn

### AI / Machine Learning
- Groq API
- LLM-based Resume Parsing
- AI Candidate Matching
- AI Skill Gap Analysis
- AI Interview Question Generation
- AI Interview Evaluation
- Groq Speech-to-Text

### Database
- PostgreSQL
- Neon

### Document Processing
- PyPDF
- python-docx

### Data & Utilities
- Pandas
- Pydantic
- Python-dotenv

### Development & Deployment
- Git
- GitHub
- Render
- uv

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │   Recruiter Portal   │
                         │      Streamlit       │
                         └──────────┬───────────┘
                                    │
                       Job Description + Resumes
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     AI Processing    │
                         │       Groq API       │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
             Match Score      Skill Gap        Interview
             & Ranking        Analysis         Questions
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                               ┌────┴─────┐
                               ▼          ▼
                     ┌──────────────┐   ┌──────────────────┐
                     │     Neon     │   │ Candidate Portal │
                     │  PostgreSQL  │   │    Streamlit     │
                     └──────────────┘   └────────┬─────────┘
                                                 │
                                    ┌────────────┼────────────┐
                                    ▼            ▼            ▼
                                Video        Voice         Text
                               Recording    Recording     Answers
                                    │            │
                                    │            ▼
                                    │      Groq Speech-to-Text
                                    │            │
                                    └────────────┼────────────┘
                                                 ▼
                                      AI Interview Evaluation
                                                 │
                                                 ▼
                                           PostgreSQL
```

---

## 📂 Project Structure

```text
TalentMatch-AI/
│
├── backend/
│   ├── main.py                  # FastAPI backend and API routes
│   └── database.py              # PostgreSQL connection and database setup
│
├── app1.py                      # Recruiter Streamlit application
├── candidate_portal.py          # Candidate interview portal
├── resume_parser.py             # Resume parsing, matching and skill-gap logic
├── interview_evaluator.py       # AI interview evaluation
├── email_service.py             # Interview email functionality
│
├── pyproject.toml               # Project dependencies
├── uv.lock                      # Locked dependency versions
├── README.md
└── .gitignore
```

---

## 🔄 How It Works

### 1. Upload Job Description

The recruiter provides a Job Description through the Recruiter Portal.

### 2. Upload Resumes

Multiple candidate resumes can be uploaded in PDF or DOCX format.

### 3. AI Resume Analysis

TalentMatch AI extracts candidate information such as:

- Name
- Skills
- Experience
- Education
- Certifications
- Projects

### 4. Candidate Matching

Each resume is analyzed against the Job Description and assigned an AI-generated match score.

Candidates are ranked based on their resume-to-role match.

### 5. Skill Gap Analysis

The system identifies:

- Matched skills
- Missing required skills
- Missing preferred skills
- Partially matched skills
- Skill-gap summary
- Recommendations

### 6. Recruiter Dashboard

Recruiters can review candidates through a dedicated dashboard containing:

- Candidate metrics
- Average resume score
- Hiring pipeline
- Candidate search and filters
- Candidate skill analysis
- Selection status

Recruiters can also mark candidates as **Selected** or **Rejected**, with the status persisted in PostgreSQL.

### 7. Interview Generation

AI generates interview questions based on the Job Description and candidate profile.

### 8. Interview Scheduling

The recruiter schedules the candidate's interview and generates a unique interview link.

### 9. Candidate Interview

The candidate opens the interview link through the Candidate Portal and answers questions using:

- Text
- Voice
- Video

### 10. Speech-to-Text

Voice responses are transcribed using Groq Speech-to-Text.

### 11. AI Interview Evaluation

The submitted interview responses are evaluated by AI.

The system generates:

- Overall Score
- Technical Knowledge
- Communication
- Problem Solving
- Strengths
- Areas for Improvement
- Recommendation
- Brief Feedback

The evaluation is stored in PostgreSQL.

---

## 📊 Example Candidate Analysis

```text
Candidate: Alice Johnson

Resume Score: 94/100

Matched Skills:
✅ Python
✅ FastAPI
✅ SQL
✅ Machine Learning

Missing Required Skills:
❌ Docker

Partially Matched Skills:
⚠️ Kubernetes

Skill Gap Summary:
Strong match for the required backend and ML skills.
Additional experience with Docker would strengthen the profile.

Selection Status:
Pending
```

---

## 🤖 Example Interview Evaluation

```text
Overall Score: 86/100

Technical Knowledge: 88/100
Communication: 84/100
Problem Solving: 86/100

Strengths:
• Strong Python fundamentals
• Good understanding of APIs
• Clear technical explanations

Areas for Improvement:
• Provide more detailed examples
• Improve system design depth

Recommendation:
Proceed to next round

Brief Feedback:
Strong technical performance with clear communication.
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Disha28r/TalentMatch-AI.git
```

### 2. Move into the project

```bash
cd TalentMatch-AI
```

### 3. Install dependencies

This project uses `uv` for dependency management.

```bash
uv sync
```

### 4. Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

### 5. Create `.env`

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

DATABASE_URL=your_postgresql_connection_string

API_BASE_URL=http://127.0.0.1:8000

CANDIDATE_PORTAL_URL=http://localhost:8502

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key

EMAIL_ADDRESS=your_email
EMAIL_APP_PASSWORD=your_email_app_password
```

> Never commit your `.env` file or expose API keys publicly.

---

## ▶️ Running the Application

### Start the FastAPI Backend

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### Start the Recruiter Portal

```bash
streamlit run app1.py
```

### Start the Candidate Portal

```bash
streamlit run candidate_portal.py --server.port 8502
```

---

## 🔐 Environment Variables

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | Groq AI and Speech-to-Text |
| `DATABASE_URL` | PostgreSQL database connection |
| `API_BASE_URL` | FastAPI backend URL |
| `CANDIDATE_PORTAL_URL` | Candidate interview portal URL |
| `QDRANT_URL` | Qdrant configuration |
| `QDRANT_API_KEY` | Qdrant authentication |
| `EMAIL_ADDRESS` | Email sender |
| `EMAIL_APP_PASSWORD` | Email authentication |

---

## ☁️ Deployment

TalentMatch AI is deployed using:

- **Render** — Application hosting
- **Neon** — PostgreSQL database
- **Groq** — AI processing and Speech-to-Text

The application is deployed as separate services:

```text
Recruiter Portal
       │
       ▼
   FastAPI Backend
       │
       ▼
 Neon PostgreSQL


Candidate Portal
       │
       ▼
   FastAPI Backend
       │
       ├── Video Upload
       ├── Interview Data
       └── Interview Evaluation
```

---
## 🎯 Use Cases

- HR Teams
- Recruiters
- Hiring Managers
- Startups
- Campus Hiring
- Recruitment Agencies

---

## ⚠️ Limitations

- AI-generated resume scores and interview evaluations may not always be fully accurate or consistent.
- The current version does not include recruiter or candidate authentication.
- Interview links currently rely on unique interview IDs rather than full user authentication.
- Interview recordings are uploaded through the application and are not yet managed through dedicated cloud storage.
- The application is designed as a functional prototype and has not yet been optimized for large-scale concurrent usage.
- AI processing can be affected by model availability, API limits, and network connectivity.
- The current system has limited automated testing and monitoring.
- AI-based candidate recommendations should support recruiter decision-making rather than replace human review.

## 🔮 Future Improvements

- Cloud storage for interview recordings
- Recruiter authentication
- Candidate authentication
- Role-based access control
- Advanced recruiter analytics
- Interview calendar integration
- Automated interview reminders
- Evaluation history and reporting
- Improved candidate recommendation workflows
- Production-grade API security

---

## 📚 What I Learned

Building TalentMatch AI gave me hands-on experience with:

- LLM integration
- Prompt engineering
- Resume parsing
- Candidate matching
- Skill-gap analysis
- FastAPI development
- REST API integration
- PostgreSQL
- Streamlit
- Browser-based media recording
- Speech-to-text
- AI interview evaluation
- Cloud deployment
- Git and GitHub
- Debugging production issues

---

## 👩‍💻 Author

### Disha R

💼 LinkedIn:

https://www.linkedin.com/in/dishar28

🐙 GitHub:

https://github.com/Disha28r

---

## ⭐ Support

If you found this project interesting, consider giving the repository a ⭐ on GitHub!
