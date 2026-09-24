from fastapi import FastAPI
from pydantic import BaseModel
from backend.database import get_connection
from psycopg.types.json import Json

app = FastAPI(
    title="TalentMatch AI API",
    description="Backend API for TalentMatch AI",
    version="1.0.0"
)

class Interview(BaseModel):

    interview_id: str
    candidate: str
    date: str
    time: str
    mode: str
    questions: list[str]
    
class InterviewEvaluation(BaseModel):
    overall_score: int
    technical_knowledge: int
    communication: int
    problem_solving: int
    strengths: list[str]
    areas_for_improvement: list[str]
    recommendation: str
    brief_feedback: str
    
class Candidate(BaseModel):
    candidate_id: str
    name: str
    resume_score: int
    resume_details: str
    matched_skills: list[str] = []
    missing_required_skills: list[str] = []
    missing_preferred_skills: list[str] = []
    partially_matched_skills: list[str] = []
    skill_gap_summary: str = ""
    recommendations: list[str] = []
    selection_status: str = "Pending"


@app.get("/")
def home():

    return {
        "message": "TalentMatch AI API is running!"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
    
@app.post("/interviews")
def create_interview(interview: Interview):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interviews (
            interview_id,
            candidate,
            interview_date,
            interview_time,
            mode,
            questions
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            interview.interview_id,
            interview.candidate,
            interview.date,
            interview.time,
            interview.mode,
            Json(interview.questions)
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Interview created successfully",
        "interview_id": interview.interview_id
    }
    
@app.get("/interviews/{interview_id}")
def get_interview(interview_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            interview_id,
            candidate,
            interview_date,
            interview_time,
            mode,
            questions
        FROM interviews
        WHERE interview_id = %s;
        """,
        (interview_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return {
            "message": "Interview not found"
        }

    return {
        "interview_id": row[0],
        "candidate": row[1],
        "date": str(row[2]),
        "time": str(row[3]),
        "mode": row[4],
        "questions": row[5]
    }
    
@app.put("/interviews/{interview_id}/evaluation")
def save_evaluation(
    interview_id: str,
    evaluation: InterviewEvaluation
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE interviews
        SET
            overall_score = %s,
            technical_knowledge = %s,
            communication = %s,
            problem_solving = %s,
            strengths = %s,
            areas_for_improvement = %s,
            recommendation = %s,
            brief_feedback = %s
        WHERE interview_id = %s;
        """,
        (
            evaluation.overall_score,
            evaluation.technical_knowledge,
            evaluation.communication,
            evaluation.problem_solving,
            Json(evaluation.strengths),
            Json(evaluation.areas_for_improvement),
            evaluation.recommendation,
            evaluation.brief_feedback,
            interview_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Evaluation saved successfully",
        "interview_id": interview_id
    }
    
    
@app.post("/candidates")
def create_candidate(candidate: Candidate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO candidates (
            candidate_id,
            name,
            resume_score,
            resume_details,
            matched_skills,
            missing_required_skills,
            missing_preferred_skills,
            partially_matched_skills,
            skill_gap_summary,
            recommendations,
            selection_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            candidate.candidate_id,
            candidate.name,
            candidate.resume_score,
            candidate.resume_details,
            Json(candidate.matched_skills),
            Json(candidate.missing_required_skills),
            Json(candidate.missing_preferred_skills),
            Json(candidate.partially_matched_skills),
            candidate.skill_gap_summary,
            Json(candidate.recommendations),
            candidate.selection_status
        )
    )

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Candidate created successfully",
        "candidate_id": candidate.candidate_id
    }
    
@app.put("/candidates/{candidate_id}/skill-gap")
def update_skill_gap(
    candidate_id: str,
    skill_gap: dict
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET
            matched_skills = %s,
            missing_required_skills = %s,
            missing_preferred_skills = %s,
            partially_matched_skills = %s,
            skill_gap_summary = %s,
            recommendations = %s
        WHERE candidate_id = %s;
        """,
        (
            Json(skill_gap["matched_skills"]),
            Json(skill_gap["missing_required_skills"]),
            Json(skill_gap["missing_preferred_skills"]),
            Json(skill_gap["partially_matched_skills"]),
            skill_gap["skill_gap_summary"],
            Json(skill_gap["recommendations"]),
            candidate_id
        )
    )

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Skill gap updated successfully",
        "candidate_id": candidate_id
    }
    
@app.get("/candidates")
def get_candidates():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            candidate_id,
            name,
            resume_score,
            resume_details,
            matched_skills,
            missing_required_skills,
            missing_preferred_skills,
            partially_matched_skills,
            skill_gap_summary,
            recommendations,
            selection_status
        FROM candidates
        ORDER BY resume_score DESC;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    candidates = []

    for row in rows:
        candidates.append({
            "candidate_id": row[0],
            "name": row[1],
            "resume_score": row[2],
            "resume_details": row[3],
            "matched_skills": row[4],
            "missing_required_skills": row[5],
            "missing_preferred_skills": row[6],
            "partially_matched_skills": row[7],
            "skill_gap_summary": row[8],
            "recommendations": row[9],
            "selection_status": row[10]
        })

    return candidates