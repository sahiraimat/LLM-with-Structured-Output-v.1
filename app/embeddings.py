from google import genai
from app.config import GEMINI_API_KEY



client = genai.Client(
    api_key=GEMINI_API_KEY 
)

EMBEDDING_MODEL = 'gemini-embedding-2'

def create_embedding(
        text: str
) -> list[float]:

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )


    return result.embeddings[0].values



