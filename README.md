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
- Generate a candidate match score
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

Recruiters can:

- Search candidates
- Filter candidates by resume score
- Filter candidates by selection status
- View candidate details
- View skill-gap analysis
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

### Programming Language

- Python

### Frontend

- Streamlit
- Browser-based media recording

### Backend

- FastAPI
- Uvicorn
- Pydantic

### AI

- Groq API
- LLM-based resume analysis
- AI candidate matching
- AI interview question generation
- Groq Speech-to-Text
- AI interview evaluation

### Database

- PostgreSQL
- Neon

### Resume Processing

- PyPDF
- python-docx

### Data & Utilities

- Pandas
- Requests
- python-dotenv

### Development & Deployment

- Git
- GitHub
- uv
- Render

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
📂 Project Structure
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
🔄 How It Works
1. Upload Job Description

The recruiter provides a Job Description through the Recruiter Portal.

2. Upload Resumes

Multiple candidate resumes can be uploaded in PDF or DOCX format.

3. Resume Analysis

The system extracts candidate information such as:

Name
Skills
Experience
Education
Certifications
Projects
4. Candidate Matching

Each resume is analyzed against the Job Description and assigned a match score.

5. Skill Gap Analysis

TalentMatch AI identifies matched, missing, and partially matched skills and generates recommendations.

6. Recruiter Dashboard

Recruiters can search and filter candidates, inspect candidate details, and export candidate information.

7. Interview Generation

AI generates interview questions based on the Job Description and candidate profile.

8. Interview Scheduling

The recruiter schedules the candidate's interview and generates a unique interview link.

9. Candidate Interview

The candidate opens the interview link and answers questions through the Candidate Portal.

Candidates can provide:

Text answers
Voice answers
Video answers
10. Speech-to-Text

Voice responses are transcribed using Groq Speech-to-Text.

11. AI Interview Evaluation

The candidate's submitted answers are evaluated by AI and the evaluation is stored in PostgreSQL.

📊 Example Candidate Analysis
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
🤖 Example Interview Evaluation
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
⚙️ Local Setup
1. Clone the repository
git clone https://github.com/Disha28r/TalentMatch-AI.git
2. Move into the project
cd TalentMatch-AI
3. Install dependencies

This project uses uv for dependency management.

uv sync
4. Activate the virtual environment

Windows:

.venv\Scripts\activate
5. Create .env

Create a .env file in the project root.

GROQ_API_KEY=your_groq_api_key

DATABASE_URL=your_postgresql_connection_string

API_BASE_URL=http://127.0.0.1:8000

CANDIDATE_PORTAL_URL=http://localhost:8502

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key

EMAIL_ADDRESS=your_email
EMAIL_APP_PASSWORD=your_email_app_password

Never commit your .env file or expose API keys publicly.

▶️ Running the Application
Start the FastAPI backend
python -m uvicorn backend.main:app --reload --port 8000
Start the Recruiter Portal
streamlit run app1.py
Start the Candidate Portal
streamlit run candidate_portal.py --server.port 8502
🔐 Environment Variables
Variable	Purpose
GROQ_API_KEY	Groq AI and Speech-to-Text
DATABASE_URL	PostgreSQL database connection
API_BASE_URL	FastAPI backend URL
CANDIDATE_PORTAL_URL	Candidate interview portal URL
QDRANT_URL	Qdrant configuration
QDRANT_API_KEY	Qdrant authentication
EMAIL_ADDRESS	Email sender
EMAIL_APP_PASSWORD	Email authentication
☁️ Deployment

TalentMatch AI is deployed using:

Render — Application hosting
Neon — PostgreSQL database
Groq — AI processing and Speech-to-Text

The application is deployed as separate services:

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
📸 Screenshots
Recruiter Dashboard
<img width="1875" height="870" alt="Recruiter Dashboard" src="https://github.com/user-attachments/assets/c32f6834-5e4d-45d0-a342-ea72962f5737" />
Resume Analysis
<img width="1428" height="712" alt="Resume Analysis" src="https://github.com/user-attachments/assets/f5eef1bc-2f5f-4d42-87b2-b8efabeda3f1" />
Candidate Ranking
<img width="1722" height="748" alt="Candidate Ranking" src="https://github.com/user-attachments/assets/68b984eb-ad66-4804-99fb-1f519d9ecf2c" />
AI-Generated Interview Questions
<img width="1528" height="856" alt="Interview Questions" src="https://github.com/user-attachments/assets/271cf67a-c01f-411a-9750-60827a3aa141" />
Candidate Interview Portal
<img width="1882" height="710" alt="Candidate Interview Portal" src="https://github.com/user-attachments/assets/423e4bf8-4864-8f7e-34349f871e32" />
🎯 Use Cases
HR Teams
Recruiters
Hiring Managers
Startups
Campus Hiring
Recruitment Agencies
🔮 Future Improvements
Cloud storage for interview recordings
Recruiter authentication
Candidate authentication
Role-based access control
Advanced recruiter analytics
Interview calendar integration
Automated interview reminders
Evaluation history and reporting
Improved candidate recommendation workflows
Production-grade API security
📚 What I Learned

Building TalentMatch AI gave me hands-on experience with:

LLM integration
Prompt engineering
Resume parsing
Candidate matching
Skill-gap analysis
FastAPI development
REST API integration
PostgreSQL
Streamlit
Browser-based media recording
Speech-to-text
AI interview evaluation
Cloud deployment
Git and GitHub
Debugging production issues
👩‍💻 Author
Disha R

💼 LinkedIn:
https://www.linkedin.com/in/dishar28

🐙 GitHub:
https://github.com/Disha28r

⭐ Support

If you found this project interesting, consider giving the repository a ⭐ on GitHub!
