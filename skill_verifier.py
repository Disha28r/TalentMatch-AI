from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Skill(BaseModel):
    name: str
    importance: str
    resume_claim: str
    verification_question: str
    
class VerificationPlan(BaseModel):
    skills: list[Skill]
    
def create_verification_plan(job_description, resume_text):

    prompt = f"""
You are an AI recruitment verification engine.

Your task is to identify the most important technical skills
that should be verified for a candidate.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

Rules:

1. Identify skills that are important for the job.
2. Prioritize skills that are required or highly relevant.
3. Only include skills that are supported by the candidate's resume
   or are clearly required by the job description.
4. For each skill, identify the candidate's relevant resume claim.
5. Assign importance as "high", "medium", or "low".
6. Do not include generic soft skills.
7. Do not create skills that are unrelated to the job.
8. Generate one technical verification question for each skill.
9. The question must test practical understanding, not simple definitions.
10. The question should relate directly to the candidate's resume claim.
11. Avoid asking the same question for overlapping skills.
12. Prefer questions that require the candidate to explain how they actually used the technology.

Return only structured JSON matching this schema:
{{
    "skills": [
        {{
            "name": "skill name",
            "importance": "high",
            "resume_claim": "candidate's relevant claim"
            "verification_question": "question that tests the candidate's actual experience"
        }}
    ]
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return VerificationPlan.model_validate_json(
        response.choices[0].message.content
    )
    
if __name__ == "__main__":

    job_description = """
    We are looking for a Backend Developer with strong Python skills.

    Requirements:
    - Python
    - FastAPI
    - REST APIs
    - PostgreSQL
    - Docker
    """

    resume_text = """
    Software Developer with experience in Python and backend development.
    Built REST APIs using FastAPI.
    Worked with PostgreSQL databases.
    Developed backend services and deployed applications using Docker.
    """

    plan = create_verification_plan(
        job_description,
        resume_text
    )

    print("\nVerification Plan:\n")

    for skill in plan.skills:
        print(f"Skill: {skill.name}")
        print(f"Importance: {skill.importance}")
        print(f"Resume Claim: {skill.resume_claim}")
        print(f"Verification Question: {skill.verification_question}")
        print("-" * 50)