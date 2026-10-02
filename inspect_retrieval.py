from app.retriever import search
from app.document_loader import load_knowledge_base


load_knowledge_base("data/knowledge.txt")

query = 'What is supervised learning?'

results = search(
    query,
    top_k=3,
    min_score=0.60
)


print("=" * 70)
print(f"QUERY: {query}")
print("=" * 70)

for result in results:

    print()
    print(f"Score: {result['score']:.4f}")
    print(f"Metadata: {result['metadata']}")
    print(f"Text: {result['text']}")