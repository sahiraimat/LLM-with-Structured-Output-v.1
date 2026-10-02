from pathlib import Path
from app.chunker import chunk_text

text = Path(
    "data/knowledge.txt"
).read_text(
    encoding="utf-8"
)

chunks = chunk_text(
    text= text,
    source="knowledge.txt",
    max_chars=500,
    overlap_sentences=1
)

for chunk in chunks:
    print("=" * 70)
    print(f"Chunk_id: {chunk.chunk_id}" )
    print(f"Source: {chunk.source}")
    print(f"Characters: {len(chunk.text)}")
    print(f"Document_id: {chunk.document_id}")
    print(f"Section: {chunk.section}")

    print()

    print(chunk.text)

    