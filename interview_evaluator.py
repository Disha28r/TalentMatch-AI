import os
import json

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

class InterviewEvaluation(BaseModel):
    overall_score: int
    technical_knowledge: int
    communication: int
    problem_solving: int
    strengths: list[str]
    areas_for_improvement: list[str]
    recommendation: str
    brief_feedback: str


def evaluate_interview(questions, answers):              

    interview_text = ""

    for i, question in enumerate(questions):

        interview_text += f"""
Question {i + 1}:
{question}

Candidate Answer:
{answers.get(i, "")}

"""


    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's interview answers below.

{interview_text}

Evaluate the candidate based on:

1. Technical Knowledge
2. Relevance of Answers
3. Communication
4. Problem Solving
5. Overall Performance

Return the evaluation as valid JSON.

Use exactly this structure:

{{
    "overall_score": 0,
    "technical_knowledge": 0,
    "communication": 0,
    "problem_solving": 0,
    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3"
    ],
    "areas_for_improvement": [
        "area 1",
        "area 2"
    ],
    "recommendation": "Recommend",
    "brief_feedback": "Short overall feedback"
}}

Rules:
- All scores must be integers between 0 and 100.
- Recommendation must be exactly one of:
  "Strongly Recommend", "Recommend", "Consider", "Do Not Recommend".
- Return only valid JSON.
- Do not include markdown or ```json code fences.
"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": "You are an expert technical interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )


    evaluation_data = json.loads(
    response.choices[0].message.content
    )

    return InterviewEvaluation(**evaluation_data)