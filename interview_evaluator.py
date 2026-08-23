import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


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

Return the evaluation in the following format:

Overall Score: <score out of 100>

Technical Knowledge: <score out of 100>

Communication: <score out of 100>

Problem Solving: <score out of 100>

Strengths:
- <strength 1>
- <strength 2>
- <strength 3>

Areas for Improvement:
- <area 1>
- <area 2>

Recommendation:
<one of: Strongly Recommend / Recommend / Consider / Do Not Recommend>

Brief Feedback:
<short overall feedback>
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


    return response.choices[0].message.content