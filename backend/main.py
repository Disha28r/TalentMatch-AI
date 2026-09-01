from fastapi import FastAPI
from pydantic import BaseModel
from backend.database import get_connection

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
            mode
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            interview.interview_id,
            interview.candidate,
            interview.date,
            interview.time,
            interview.mode
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Interview created successfully",
        "interview_id": interview.interview_id
    }