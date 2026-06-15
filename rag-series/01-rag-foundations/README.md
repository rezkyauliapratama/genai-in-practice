# RAG #1 - Foundations

> Part 1 of 6 of the **RAG Full Stack Series**

**Article:** [Why Your LLM Needs a Library: RAG Fundamentals for the Pragmatic Engineer](https://linkedin.com/in/rezkyauliapratama)

---

## Prerequisites

UV must be installed at the repo root level. See [root README](../../README.md#prerequisites) for installation steps.

```bash
# From the repo root - run once
uv sync --extra dev
cp .env.example .env   # fill in LLM_PROVIDER and API key
```

---

## Running the Pipeline

### Option 1 - From the module folder (recommended)

```bash
cd rag-series/01-rag-foundations
uv run python -m src.pipeline
```

This starts an interactive REPL loop:

```
Indexed 42 chunks. RAG pipeline ready. Type 'exit' to quit.

Your question: how do I block my card?

To block your card immediately, you can either call 1500-153 or use
the mobile banking app under Settings > Card Management > Block Card.
Confirmation is sent to your registered email.

Your question: exit
```

### Option 2 - From repo root via Makefile

```bash
make run MODULE=01-rag-foundations
```

### Option 3 - Jupyter notebook (interactive step-by-step)

```bash
# From repo root
uv run jupyter lab
# Then open: rag-series/01-rag-foundations/notebooks/01_rag_foundations.ipynb
```

---

## Swapping to Qdrant (Level Up)

The in-memory vector store is good for learning. For production-grade persistence, swap to Qdrant in two steps:

**Step 1 - Start Qdrant locally:**

```bash
docker run -p 6333:6333 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

**Step 2 - Edit `src/pipeline.py`, uncomment the Qdrant lines:**

```python
# BEFORE (in-memory)
from src.vector_store import InMemoryVectorStore
self.store = InMemoryVectorStore()

# AFTER (Qdrant) - just swap these two lines
from src.qdrant_store import QdrantVectorStore
self.store = QdrantVectorStore()
```

Re-run the pipeline. The knowledge base is now persisted to disk and survives restarts.

---

## Folder Structure

```
01-rag-foundations/
├── README.md
├── data/                          ← knowledge base (markdown files)
│   ├── cards.md
│   ├── transfers.md
│   ├── accounts.md
│   └── compliance.md
├── notebooks/
│   └── 01_rag_foundations.ipynb   ← interactive step-by-step version
└── src/
    ├── __init__.py
    ├── chunker.py                 ← load + split documents
    ├── embedder.py                ← text -> vectors
    ├── vector_store.py            ← in-memory store (learn here first)
    ├── qdrant_store.py            ← Qdrant store (level up)
    ├── retriever.py               ← top-K + score threshold
    ├── generator.py               ← prompt template + LLM call
    └── pipeline.py                ← RAGPipeline orchestrator
```

---

## Component Map

| RAG Component | Module | Responsibility |
|---|---|---|
| Knowledge Base | `data/` + `chunker.py` | Load markdown docs, split into chunks |
| Embedding Model | `embedder.py` | Text -> vectors |
| Vector Database | `vector_store.py` | Store vectors, similarity search |
| Retriever | `retriever.py` | Top-K search with a relevance gate |
| Orchestrator | `generator.py` + `pipeline.py` | Prompt augmentation, LLM call, glue |

---

## Suggested Test Queries

| Query | What It Tests |
|---|---|
| `"how do I block my card?"` | Direct match - straightforward retrieval |
| `"how to freeze my debit card"` | Semantic match - same intent, different words |
| `"BI-FAST limit"` | Partial phrase match across heading and body |
| `"what documents for new account"` | Multi-concept query - top-K aggregation |
| `"what is the capital of France?"` | Out-of-scope - tests both refusal layers |
