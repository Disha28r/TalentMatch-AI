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

    return {
        "message": "Interview created successfully",
        "interview": interview
    }
    
@app.get("/interviews")
def get_interviews():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            interview_id,
            candidate,
            interview_date,
            interview_time,
            mode
        FROM interviews
        ORDER BY interview_date, interview_time;
    """)

    rows = cursor.fetchall()

    interviews = []

    for row in rows:
        interviews.append({
            "interview_id": row[0],
            "candidate": row[1],
            "date": str(row[2]),
            "time": str(row[3]),
            "mode": row[4]
        })

    cursor.close()
    connection.close()

    return {
        "interviews": interviews
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
            mode
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
        "mode": row[4]
    }