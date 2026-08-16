# Agent Series #01 — Multi-Agent Systems

Companion code untuk artikel **Agent Series #1: Multi-Agent Systems** (OKR G1-Q3-08, gap P0: Multi-Agent Systems).

Praktik 3 framework/pattern dalam satu module:
- **LangGraph Supervisor** — routing dinamis (supervisor + researcher + summarizer), loop guard
- **Google ADK** — agent hierarchy (root + sub-agents), delegasi otomatis
- **LangGraph Pipeline** — 2-agent sekuensial (research -> summarize) + error handling

## Struktur

```
agent-series/01-multi-agent-systems/
├── README.md
├── .env.example          # copy ke .env
├── requirements.txt
├── Dockerfile            # build image container
├── docker-compose.yml    # jalan via compose
├── src/
│   ├── config.py                   # baca env (DeepSeek)
│   ├── langgraph_supervisor.py     # Task 2: supervisor workflow
│   ├── google_adk_agents.py        # Task 3: ADK hierarchy
│   ├── research_summarize.py       # Task 4: pipeline + error handling
│   └── main.py                     # CLI entrypoint
└── docs/
    ├── refleksi.md                 # jawaban 5 pertanyaan refleksi
    └── multiagent-cheatsheet.md    # cheat sheet 1 halaman
```

## Quick Start (Lokal)

```bash
# 1. venv + deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. env
cp .env.example .env
# isi DEEPSEEK_API_KEY (atau provider OpenAI-compatible lain)

# 3. jalankan salah satu demo
python -m src.main --demo langgraph   # Task 2: supervisor
python -m src.main --demo adk         # Task 3: ADK multi-agent
python -m src.main --demo pipeline    # Task 4: 2-agent pipeline
python -m src.main --demo all         # semua demo berurutan
```

## Quick Start (Docker)

```bash
# build image
docker compose build

# jalankan semua demo (perlu .env berisi DEEPSEEK_API_KEY)
docker compose up

# atau satu demo
docker compose run --rm multi-agent python -m src.main --demo langgraph
```

## Desain

- Model: DeepSeek via OpenAI-compatible API (default), bisa diganti di `src/config.py`
- Tool `web_search` = dummy (tanpa API key search) supaya demo bisa jalan offline
- Supervisor pakai `Command(goto=...)` + loop guard max 5 iterasi (anti infinite loop)
- ADK pakai `FunctionTool`, `Runner.run` generator events, `create_session` async (API ADK >= 2.7)
- Error handling: try/except di research node + fallback data

## Catatan Versi (16 Agu 2026)

- LangGraph 1.x: `create_react_agent` deprecated -> `langchain.agents.create_agent` (warning, masih jalan)
- ADK 2.7: `function_tool` bukan decorator -> `FunctionTool(func=...)`; `Runner.run` = generator events (`new_message=Content(...)`); `create_session` async; model provider-style butuh `pip install litellm`
