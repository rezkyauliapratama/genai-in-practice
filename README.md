# GenAI in Practice

A companion repository for the **GenAI in Practice** series - each article is a self-contained module; shared utilities are written once and reused throughout.

> **Package manager:** This project uses [UV](https://docs.astral.sh/uv/) - a blazing-fast Python package manager written in Rust. UV replaces `pip`, `venv`, and `pip-tools` in a single tool.

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| UV | latest | See below |

### Install UV

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or via pip (not recommended - defeats the purpose):**
```bash
pip install uv
```

Verify installation:
```bash
uv --version
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/rezkyauliapratama/genai-in-practice
cd genai-in-practice

# 2. Create .venv and install all dependencies (UV auto-creates .venv)
uv sync --extra dev

# 3. Configure environment
cp .env.example .env
# Open .env and fill in your LLM API key + pick your provider

# 4. Run a module
cd rag-series/01-rag-foundations
uv run python -m src.pipeline
```

> UV auto-detects `pyproject.toml` at the repo root. You do NOT need to activate the virtual environment manually - `uv run` handles it.

---

## UV Cheat Sheet

| Task | Command |
|---|---|
| Create venv + install deps | `uv sync` |
| Install with dev deps | `uv sync --extra dev` |
| Add a new dependency | `uv add <package>` |
| Add a dev dependency | `uv add --dev <package>` |
| Remove a dependency | `uv remove <package>` |
| Run a script inside venv | `uv run python script.py` |
| Run a module | `uv run python -m module.name` |
| Run a CLI tool (e.g. ruff) | `uv run ruff check .` |
| Start Jupyter | `uv run jupyter lab` |
| Update all packages | `uv lock --upgrade` |
| Show installed packages | `uv pip list` |

---

## Environment Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```ini
# LLM Provider: openai | gemini | groq
LLM_PROVIDER=openai

# API Keys - fill in only the provider you use
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=
GROQ_API_KEY=

# Embedding Provider: huggingface | openai
# huggingface = local model (free, no API key needed)
# openai = uses text-embedding-3-small (billed)
EMBEDDING_PROVIDER=huggingface

# Logging
LOG_LEVEL=INFO
```

**Provider Guide:**

| Provider | Free Tier | Model Used | Notes |
|---|---|---|---|
| `openai` | No | `gpt-4o-mini` | Fastest to set up |
| `gemini` | Yes (rate limited) | `gemini-2.0-flash` | Google AI Studio key |
| `groq` | Yes (rate limited) | `llama-3.1-70b-versatile` | Fastest inference |

> For embeddings, `huggingface` is recommended for local development - it downloads `all-MiniLM-L6-v2` (~80MB) on first run and runs on CPU with no API cost.

---

## Project Structure

```
genai-in-practice/
│
├── rag-series/
│   └── 01-rag-foundations/          ← RAG #1: Foundations
│       ├── README.md
│       ├── data/                    ← knowledge base (markdown files)
│       └── src/                     ← pipeline modules
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

---

## Makefile Shortcuts

```bash
make setup                         # uv sync --extra dev
make run MODULE=01-rag-foundations # run a specific module
make lint                          # ruff check
make format                        # ruff format
make test                          # pytest
```

---

## Series Index

| # | Article | Status |
|---|---------|--------|
| 01 | RAG Foundations | ✅ Published |

---

## Author

**Rezky Aulia Pratama** - Solution Architect, Banking Industry  
[linkedin.com/in/rezkyauliapratama](https://linkedin.com/in/rezkyauliapratama) | [medium.com/@rezkyauliapratama](https://medium.com/@rezkyauliapratama)
