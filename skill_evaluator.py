from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class SkillEvaluation(BaseModel):
    skill: str
    confidence: float
    status: str
    evidence: str
    follow_up_needed: bool


def evaluate_skill(
    skill,
    resume_claim,
    question,
    candidate_answer
):

    prompt = f"""
You are an AI skill verification evaluator.

Your job is to determine whether a candidate has provided
credible evidence supporting a skill claimed on their resume.

SKILL:
{skill}

RESUME CLAIM:
{resume_claim}

VERIFICATION QUESTION:
{question}

CANDIDATE ANSWER:
{candidate_answer}

Evaluate the answer based on demonstrated evidence,
not merely whether the candidate knows the definition.

Evaluation rules:

1. Determine whether the answer demonstrates practical
   understanding or experience with the claimed skill.

2. A definition-only answer should not receive high confidence.

3. Strong, specific and technically accurate evidence should
   receive higher confidence.

4. Do not assume experience that the candidate did not demonstrate.

5. Confidence must be between 0 and 1.

6. Use these statuses:
   - "verified" → strong evidence
   - "partial" → some evidence but insufficient or incomplete
   - "unverified" → little or no credible evidence

7. Set follow_up_needed to true when the evidence is insufficient
   and a follow-up question would help verify the skill.

Return only JSON in this format:

{{
    "skill": "skill name",
    "confidence": 0.0,
    "status": "verified",
    "evidence": "brief explanation of the evidence demonstrated",
    "follow_up_needed": false
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

    return SkillEvaluation.model_validate_json(
        response.choices[0].message.content
    )
    
def generate_follow_up(
    skill,
    resume_claim,
    original_question,
    candidate_answer,
    evidence
):

    prompt = f"""
You are an adaptive AI skill verification interviewer.

The candidate has claimed the following skill:

SKILL:
{skill}

RESUME CLAIM:
{resume_claim}

ORIGINAL QUESTION:
{original_question}

CANDIDATE ANSWER:
{candidate_answer}

EVALUATION EVIDENCE:
{evidence}

The candidate has not provided enough evidence to confidently
verify the claimed skill.

Generate ONE targeted follow-up question.

Rules:

1. The question must directly address the missing evidence.
2. Do not repeat the original question.
3. Do not ask a generic definition question.
4. Ask for a concrete example, implementation detail,
   decision, problem, or experience.
5. Keep the question concise.
6. The goal is to determine whether the candidate actually
   has practical experience with the claimed skill.

Return only JSON:

{{
    "follow_up_question": "..."
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

    return json.loads(response.choices[0].message.content)["follow_up_question"]

