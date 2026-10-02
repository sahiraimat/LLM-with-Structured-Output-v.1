from pathlib import Path
from app.chunker import chunk_text
from app.retriever import add_document


def load_knowledge_base(
        path: str
):
    text = Path(path).read_text(
        encoding="utf-8"
    )

    document_id = Path(path).stem

    chunks = chunk_text(
        text=text,
        source=path,
        max_chars=1000,
        overlap_sentences=1
        )

    for chunk in chunks:
        add_document(
            text=chunk.text,
            metadata={
                "document_id": document_id,
                "source": chunk.source,
                "chunk_id": chunk.chunk_id,
                "section": chunk.section
            }
            
        )

    return len(chunks)
