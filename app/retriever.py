import math 
from app.embeddings import create_embedding


DOCUMENTS = []

def cosine_similarity(
        a: list[float],
        b: list[float]
) -> float:

    dot_product = sum(
        x * y 
        for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
            sum(x * x for x in b)
        )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )

def add_document(
        text: str,
        metadata: dict
):
    embedding = create_embedding(text)

    DOCUMENTS.append(
        {
            "text": text,
            "embedding": embedding,
            "metadata": metadata
        }
    )

def search(
        query: str,
        top_k: int = 3,
        min_score: float = 0.60
):
    query_embedding = create_embedding(
        query
    )

    results = []

    for document in DOCUMENTS:

        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )

        if score < min_score:
            continue

        results.append({
            "text": document["text"],
            "score": score,
            "metadata": document["metadata"]
        })

    results.sort(
        key= lambda x: x["score"],
        reverse=True
        )

    return results[:top_k]

    
