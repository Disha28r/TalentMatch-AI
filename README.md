# 🎯 TalentMatch AI

An AI-powered Resume Screening & Candidate Ranking system that helps recruiters quickly evaluate resumes against a job description using Large Language Models (LLMs).

TalentMatch AI analyzes resumes, extracts structured information, calculates candidate-job match scores, ranks applicants, and even generates personalized interview questions for the top candidates.

---

## 🚀 Features

- 📄 Upload a Job Description
- 📂 Upload multiple resumes (PDF/DOCX)
- 🤖 AI-powered resume parsing using Groq LLM
- 🎯 AI-based candidate-job matching
- 📊 Match score calculation (0–100)
- 🏆 Automatic candidate ranking
- ⭐ Displays Top Candidates
- 📉 Identifies Lowest Matching Candidates
- 💬 AI-generated interview questions for shortlisted candidates
- 🌐 Interactive Streamlit interface

---

## 🛠 Tech Stack

### Programming Language
- Python

### Framework
- Streamlit

### AI Model
- Groq API
- OpenAI GPT OSS 120B / Llama 3.3 (configurable)

### Libraries
- Pydantic
- PyPDF
- python-docx
- python-dotenv
- pathlib
- tempfile
- json

---

## 📂 Project Structure

```
TalentMatch-AI/
│
├── app1.py                 # Streamlit UI
├── resume_parser.py        # AI parsing & scoring logic
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
└── requirements.txt (optional)
```

---

## ⚙️ How It Works

### Step 1

Upload a Job Description.

↓

### Step 2

Upload multiple resumes.

↓

### Step 3

The AI extracts structured information including:

- Name
- Skills
- Experience
- Education
- Certifications
- Projects

↓

### Step 4

Each resume is compared against the Job Description.

↓

### Step 5

TalentMatch AI calculates a compatibility score.

↓

### Step 6

Candidates are ranked automatically.

↓

### Step 7

The top candidates receive AI-generated interview questions tailored to their profile.

---

## 📊 Example Output

```
Candidate Rankings

🥇 Alice Johnson — 94/100

🥈 Bob Smith — 89/100

🥉 Charlie Davis — 81/100

Lowest Matching Candidates

David — 56/100

Emma — 48/100
```

---

## 💡 Future Improvements

- Export results to CSV/Excel
- Resume Skill Gap Analysis
- Resume Improvement Suggestions
- Candidate Comparison Dashboard
- Recruiter Authentication
- Database Integration
- ATS Resume Compliance Checker
- Resume Similarity Search using Vector Database
- Multi-language Resume Support
- Email shortlisted candidates automatically

---

## 🖥 Installation

Clone the repository

```bash
git clone https://github.com/Disha28r/TalentMatch-AI.git
```

Move into the project

```bash
cd TalentMatch-AI
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
```

Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 📸 Screenshots

<img width="1875" height="870" alt="image" src="https://github.com/user-attachments/assets/c32f6834-5e4d-45d0-a342-ea72962f5737" />
<img width="1428" height="712" alt="image" src="https://github.com/user-attachments/assets/f5eef1bc-2f5f-4d42-87b2-b8efabeda3f1" />
Ranking:
<img width="1722" height="748" alt="image" src="https://github.com/user-attachments/assets/68b984eb-ad66-4804-99fb-1f519d9ecf2c" />
Top 2 candidates are picked and alloted 5 interview questions based on JD
<img width="1528" height="856" alt="image" src="https://github.com/user-attachments/assets/271cf67a-c01f-411a-9750-60827a3aa141" />
<img width="1882" height="710" alt="image" src="https://github.com/user-attachments/assets/423e4bf8-4868-4f7e-8fb7-34349f871e32" />






Example:

- Upload Screen
- Candidate Ranking
- AI Interview Questions

---

## 🎯 Use Cases

- HR Teams
- Recruiters
- Hiring Managers
- Startups
- Campus Hiring
- Recruitment Agencies

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve TalentMatch AI:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 👩‍💻 Author

**Disha R**

- GitHub: https://github.com/Disha28r
- LinkedIn: *(Add your LinkedIn profile here)*

---

## ⭐ If you found this project useful...

Please consider giving it a ⭐ on GitHub!
