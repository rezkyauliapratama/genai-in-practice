# src/chunker.py
# Component #1 - Knowledge Base loader and splitter.
# Loads markdown files from data/ and splits them into retrievable chunks.
# Each chunk carries metadata (source, chunk_index) used later for citations
# and Qdrant payload filtering.
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_dir: str = "data") -> list[dict]:
    """Read all .md files in data_dir and return as a list of dicts."""
    return [
        {"source": path.name, "text": path.read_text(encoding="utf-8")}
        for path in sorted(Path(data_dir).glob("*.md"))
    ]


def chunk_documents(
    docs: list[dict],
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[dict]:
    """Split documents into chunks.

    Separator priority (highest to lowest):
      \\n##  - prefer to split at markdown section headings
      \\n\\n - then at paragraph breaks
      \\n   - then at line breaks
      ' '   - last resort: word boundary

    chunk_size=512 chars keeps each chunk to ~1 FAQ entry.
    chunk_overlap=50 prevents a sentence on a boundary from being lost.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n\n", "\n", " "],
    )
    chunks = []
    for doc in docs:
        for i, text in enumerate(splitter.split_text(doc["text"])):
            chunks.append({
                "doc_id": f"{doc['source']}::chunk-{i}",
                "content": text,
                "metadata": {"source": doc["source"], "chunk_index": i},
            })
    return chunks
