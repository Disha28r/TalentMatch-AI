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