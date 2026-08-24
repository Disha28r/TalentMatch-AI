from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="TalentMatch AI API",
    description="Backend API for TalentMatch AI",
    version="1.0.0"
)

class Interview(BaseModel):

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