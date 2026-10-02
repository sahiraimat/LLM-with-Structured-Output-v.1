from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.schemas import AIAnswer, EducationalAnswer


client = genai.Client(api_key=GEMINI_API_KEY)



### Use this for LLM with structured output (No RAG)
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



### use this for RAG enabled LLM

def generate_rag_response(
        question: str,
        context: str
) -> str:

    prompt = f"""

    You are a helpful AI assistant.

    Answer the user's question using only the
    provided context.

    Rules:
    1. Do not invent information.
    2. If the answer is not supported by the context, say so.
    3. use the source information to support your answer.
    4. Do not claim information came from a source unless it is present in that source.


    CONTEXT:
    {context}

    QUESTION:
    {question}
    
    """
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )


    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text


