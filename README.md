# GenAI in Practice

A companion repository for the **GenAI in Practice** series. Each article is a self-contained module; shared utilities are written once and reused throughout.

## Structure

```
genai-in-practice/
│
├── rag-series/
│   └── 01-rag-foundations/          ← RAG #1: Foundations
│
├── _shared/                         ← reused by every module
│   ├── config.py
│   ├── llm_client.py
│   └── utils.py
│
├── .env.example
├── .gitignore
├── Makefile
├── pyproject.toml
└── README.md
```

## Quick Start

```bash
git clone https://github.com/rezkyauliapratama/genai-in-practice
cd genai-in-practice
make setup
cp .env.example .env   # add your API key, pick your provider

cd rag-series/01-rag-foundations
python -m src.pipeline
```

## Series Index

| # | Article | Status |
|---|---------|--------|
| 01 | RAG Foundations | ✅ Published |

## Author

**Rezky Aulia Pratama** - Solution Architect, Banking Industry  
[linkedin.com/in/rezkyauliapratama](https://linkedin.com/in/rezkyauliapratama) | [medium.com/@rezkyauliapratama](https://medium.com/@rezkyauliapratama)
