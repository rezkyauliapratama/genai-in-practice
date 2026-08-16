"""Task 4 — 2-Agent Pipeline (Research + Summarize) + Error Handling.

Alur: query -> [RESEARCH: web search] -> notes -> [SUMMARIZE: LLM] -> summary
Pendekatan: pipeline sekuensial (LangGraph StateGraph).
"""
from typing import TypedDict

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from .config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_CHAT_MODEL, check_env


class State(TypedDict, total=False):
    query: str
    notes: str
    summary: str


@tool
def search_web(q: str) -> str:
    """Search web (dummy untuk tes; ganti dengan API search asli)."""
    return (
        f"Hasil riset untuk '{q}': "
        "Multi-agent: pecah task kompleks ke agent spesialis. "
        "Pattern utama: orchestrator (terpusat), supervisor (dinamis), swarm (peer). "
        "Tool-calling + shared state adalah fondasi koordinasi. "
        "Framework: LangGraph (graph), CrewAI (crew), ADK (hierarchy)."
    )


def build_pipeline():
    """Build 2-agent pipeline: research -> summarize."""
    check_env()
    model = ChatOpenAI(
        model=DEEPSEEK_CHAT_MODEL,
        base_url=DEEPSEEK_BASE_URL,
        api_key=DEEPSEEK_API_KEY,
        temperature=0.3,
    )

    def research_node(state: State) -> State:
        """Node research: panggil tool search, simpan notes. Ada error handling."""
        try:
            notes = search_web.invoke(state["query"])
            return {"notes": notes}
        except Exception as e:
            return {"notes": f"ERROR: {e}. Pakai data fallback: multi-agent = koordinasi agent spesialis."}

    def summarize_node(state: State) -> State:
        """Node summarize: LLM murni, ringkas jadi 3 poin."""
        resp = model.invoke(f"Ringkas jadi 3 poin padat: {state['notes']}")
        return {"summary": resp.content}

    graph = StateGraph(State)
    graph.add_node("research", research_node)
    graph.add_node("summarize", summarize_node)
    graph.add_edge("research", "summarize")
    graph.add_edge("summarize", END)
    graph.set_entry_point("research")
    return graph.compile()


def run_pipeline():
    """Jalankan pipeline untuk 3 query."""
    app = build_pipeline()
    queries = [
        "Multi-agent vs single agent: kapan pilih apa?",
        "Apa itu RAG?",
        "Kapan pakai supervisor pattern?",
    ]
    for i, q in enumerate(queries, 1):
        print(f"\n{'='*50}\nQUERY {i}: {q}\n{'='*50}")
        out = app.invoke({"query": q})
        print("NOTES:", out["notes"][:120], "...")
        print("SUMMARY:")
        print(out["summary"])


if __name__ == "__main__":
    run_pipeline()
