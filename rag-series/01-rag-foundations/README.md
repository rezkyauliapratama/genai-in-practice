# RAG #1 - Foundations

> Part 1 of 6 of the **RAG Full Stack Series**

**Article:** [Why Your LLM Needs a Library: RAG Fundamentals for the Pragmatic Engineer](https://linkedin.com/in/rezkyauliapratama)

## What You Will Build

A fully working, modular RAG pipeline - one Python file per component - that goes from raw markdown documents all the way to grounded, auditable answers. In the second half, you swap the in-memory vector store for Qdrant with a single line change.

## Folder Structure

```
01-rag-foundations/
├── README.md
├── data/                          <- knowledge base (markdown files)
│   ├── cards.md
│   ├── transfers.md
│   ├── accounts.md
│   └── compliance.md
├── notebooks/
│   └── 01_rag_foundations.ipynb   <- step-by-step interactive version
└── src/
    ├── __init__.py
    ├── chunker.py                 <- load + split documents
    ├── embedder.py                <- text -> vectors
    ├── vector_store.py            <- in-memory store
    ├── qdrant_store.py            <- Qdrant store
    ├── retriever.py               <- top-K + score threshold
    ├── generator.py               <- prompt template + LLM call
    └── pipeline.py                <- RAGPipeline orchestrator
```

## Component Map

| RAG Component | Module | Responsibility |
|---|---|---|
| Knowledge Base | `data/` + `chunker.py` | Load markdown docs, split into chunks |
| Embedding Model | `embedder.py` | Text -> vectors |
| Vector Database | `vector_store.py` | Store vectors, similarity search |
| Retriever | `retriever.py` | Top-K search with a relevance gate |
| Orchestrator | `generator.py` + `pipeline.py` | Prompt augmentation, LLM call, glue |

## Quick Start

```bash
# From repo root
make setup
cp .env.example .env   # fill in your API key and provider

cd rag-series/01-rag-foundations
python -m src.pipeline
```

### Manual install (Python 3.11+)

```bash
pip install sentence-transformers langchain-text-splitters openai pydantic-settings numpy
```

### With Qdrant (Level Up section)

```bash
# 1. Start Qdrant
docker run -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant

# 2. Install client
pip install qdrant-client

# 3. In pipeline.py, swap InMemoryVectorStore -> QdrantVectorStore
```

## Suggested Test Queries

| Query | What It Tests |
|---|---|
| `"how do I block my card?"` | Direct match: straightforward retrieval |
| `"how to freeze my debit card"` | Semantic match: same intent, different words |
| `"BI-FAST limit"` | Partial phrase match across heading and body |
| `"what documents for new account"` | Multi-concept query: top-K aggregation |
| `"what is the capital of France?"` | Out-of-scope: tests both refusal layers |
