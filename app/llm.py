from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.schemas import AIAnswer, EducationalAnswer


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_structured_response(
        topic: str,
        level: str
) -> EducationalAnswer:

    prompt = f"""
    Teach the following topic.

    Topic: {topic}
    Student level: {level}

    Explain it clearly and provide useful examples.
    """

    response=client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "response_mime_type":"application/json",
            "response_schema": EducationalAnswer,
        },
    )

    if not response.parsed:
        raise RuntimeError(
            "Gemini did not return structured output."
        )
    
    return response.parsed


