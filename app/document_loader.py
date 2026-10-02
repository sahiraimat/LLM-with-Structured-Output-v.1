from pathlib import Path
from app.chunker import chunk_text
from app.retriever import add_document


def load_knowledge_base(
        path: str
):

    file_path = Path(path)

    text = file_path.read_text(
        encoding="utf-8"
    )

    document_id = file_path.stem

    chunks = chunk_text(
        text=text,
        document_id=document_id,
        source=str(file_path),
        max_chars=1000,
        overlap_sentences=1
        )

    for chunk in chunks:
        add_document(
            text=chunk.text,
            metadata={
                "document_id": chunk.document_id,
                "source": chunk.source,
                "chunk_id": chunk.chunk_id,
                "section": chunk.section
            }
            
        )

    return len(chunks)
