# Multi-Agent Cheat Sheet (Task 5)

> Ringkasan 1 halaman dari praktik LangGraph + ADK, 16 Agu 2026

## 5 Konsep Kunci

- Agent = LLM + prompt + tools + loop (think -> act -> observe)
- State = data bersama yang mengalir antar node/agent (TypedDict di LangGraph)
- Tool-calling = LLM minta eksekusi fungsi eksternal, hasil balik ke LLM
- Orchestrator = routing fixed, worker tidak mengubah alur
- Supervisor = routing dinamis, evaluasi tiap step, bisa loop sampai FINISH

## 3 Snippet Paling Sering Dipakai

1. Supervisor routing dinamis (LangGraph):
```python
from langgraph.types import Command
def supervisor_node(state):
    decision = model.invoke([...]).content.strip().upper()
    return Command(goto=decision.lower(), update={"iterations": n})
```

2. Node + edge pipeline (LangGraph):
```python
graph = StateGraph(State)
graph.add_node("research", research_node)
graph.add_edge("research", "summarize")
graph.set_entry_point("research")
app = graph.compile()
```

3. Sub-agent ADK (hierarchy):
```python
root = Agent(name="root", model=MODEL, sub_agents=[researcher, summarizer])
# Runner.run(user_id=..., session_id=..., new_message=Content(parts=[Part(text=msg)]))
```

## 3 Error Umum + Fix (dari praktik)

- `create_react_agent` deprecated (LangGraph 1.x): pindah ke `langchain.agents.create_agent`; masih jalan tapi warning.
- ADK 2.7: `function_tool` bukan decorator lagi -> `FunctionTool(func=...)`; `Runner.run` = generator events (bukan return message) + butuh `new_message=Content(...)`; `create_session` = async -> `asyncio.run(...)`.
- Model provider-style ADK (`deepseek/...`) butuh `pip install litellm` (google-adk[extensions]).
- Supervisor loop tak berhenti -> loop guard: `if iterations > 5: return Command(goto="finish")`.

## Pola Pilih Framework

- Pipeline fixed: LangGraph edges / ADK sub-agents
- Routing dinamis: LangGraph supervisor + Command(goto)
- Prototype cepat: ADK
- Kontrol halus (loop/retry/HITL): LangGraph

## Anti-Pattern

- Multi-agent untuk task sederhana | tanpa loop guard | state raksasa | tool call tanpa try/except | semua agent model mahal
