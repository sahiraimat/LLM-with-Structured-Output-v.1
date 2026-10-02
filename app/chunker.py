import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    chunk_id: int
    document_id: str
    source: str
    section: str | None = None



def split_sentences(text: str) -> list[str]:
    """Split text into sentences."""

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()

    ]


def chunk_text(
        text: str,
        document_id: str,
        source: str,
        max_chars: int = 1000,
        overlap_sentences: int = 1
) -> list[Chunk]:


    lines = text.splitlines()
    
    chunks: list[Chunk] = []
    current_sentences: list[str] = []
    current_section: str | None = None
    chunk_id = 0

    for line in lines:

        line = line.strip()

        if not line:
            continue

        #Detect Markdown headings

        heading_match = re.match(
            r"^#{1,3}\s+(.+)",
            line
        )

        if heading_match:
            current_section = heading_match.group(1).strip()
            continue

        sentences = split_sentences(line)


        for sentence in sentences:
            candidate = " ".join(
                current_sentences + [sentence]
            )

            if (
                current_sentences and len(candidate) > max_chars
            ):
                chunks.append(
                    Chunk(
                        text=" ".join(current_sentences),
                        chunk_id=chunk_id,
                        source=source,
                        document_id=document_id,
                        section=current_section
                    )
                )
                chunk_id +=1 

                current_sentences = (
                    current_sentences[-overlap_sentences:]
                )

            current_sentences.append(sentence)

        if current_sentences:

            chunks.append(
                Chunk(
                    text = " ".join(
                        current_sentences
                    ),
                    chunk_id=chunk_id,
                    source=source,
                    document_id= document_id,
                    section=current_section
                )
            )
        chunk_id += 1 
        current_sentences = (
            current_sentences[-overlap_sentences:]
        )

    return chunks
    







# def chunk_text(
#         text: str,
#         chunk_size: int = 500,
#         overlap: int = 100
# ) -> list[str]:

#     if overlap >= chunk_size:
#         raise ValueError(
#             "Overlap must be smaller than chunk_size."
#         )

#     chunks = []

#     start = 0 

#     while start < len(text):
#         end = start + chunk_size
#         chunk=text[start:end].strip()

#         if chunk:
#             chunks.append(chunk)

#         start += chunk_size - overlap

#     return chunks
