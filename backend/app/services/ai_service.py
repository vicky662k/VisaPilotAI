from openai import OpenAI
from openai import OpenAIError

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def parse_resume_with_ai(text: str):

    prompt = f"""
You are an expert ATS resume parser.

Extract the following fields.

Return ONLY valid JSON.

{{
"name":"",
"email":"",
"phone":"",
"current_company":"",
"job_title":"",
"experience_years":"",
"skills":[],
"education":[],
"certifications":[],
"languages":[]
}}

Resume:

{text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content

    except OpenAIError as e:
        return {
            "status": "OpenAI unavailable",
            "reason": str(e),
            "raw_text": text,
        }