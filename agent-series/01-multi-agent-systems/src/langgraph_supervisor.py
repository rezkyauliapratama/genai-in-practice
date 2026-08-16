"""Task 2 — LangGraph Supervisor Workflow (Research + Summarize).

Supervisor (LLM) memutuskan routing dinamis:
  researcher  -> web search (dummy tool untuk tes)
  summarizer  -> LLM murni, ringkas notes
  finish      -> output final
Loop guard: max 5 iterasi supervisor.
"""
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from .config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_CHAT_MODEL, check_env


# --- State ---
class AgentState(TypedDict, total=False):
    messages: Annotated[list, "messages"]  # chat history
    query: str
    research_notes: str
    summary: str
    iterations: int


# --- Tools (dummy untuk tes, tanpa API key search) ---
@tool
def web_search(query: str) -> str:
    """Cari informasi terkini di web."""
    return (
        f"[hasil search untuk: {query}] "
        "Multi-agent systems 2026: orchestrator/supervisor patterns dominan, "
        "MCP + A2A jadi standar interoperabilitas, enterprise adoption naik ke ~40%."
    )


def build_graph():
    """Build dan compile supervisor graph."""
    check_env()
    model = ChatOpenAI(
        model=DEEPSEEK_CHAT_MODEL,
        base_url=DEEPSEEK_BASE_URL,
        api_key=DEEPSEEK_API_KEY,
        temperature=0.3,
    )

    # --- Workers ---
    researcher = create_react_agent(model, tools=[web_search])
    summarizer = create_react_agent(model, tools=[])

    # --- Nodes ---
    def supervisor_node(state: AgentState):
        """LLM memilih agent berikutnya; loop guard max 5 iterasi."""
        iterations = state.get("iterations", 0) + 1
        if iterations > 5:
            return Command(goto="finish")

        notes = state.get("research_notes", "")
        route = model.invoke([
            HumanMessage(content=f"""
            Kamu supervisor. Pilih agent berikutnya. Jawab HANYA satu kata:
            - "researcher": jika butuh informasi tambahan (query: {state['query']})
            - "summarizer": jika research_notes sudah cukup
            - "finish": jika sudah selesai
            Research notes saat ini: {notes or '(kosong)'}
            """)
        ])
        decision = route.content.strip().upper()
        if decision not in ("RESEARCHER", "SUMMARIZER", "FINISH"):
            decision = "RESEARCHER"  # fallback aman
        return Command(goto=decision.lower(), update={"iterations": iterations})

    def researcher_node(state: AgentState) -> AgentState:
        result = researcher.invoke({
            "messages": [HumanMessage(content=f"Research: {state['query']}")]
        })
        notes = result["messages"][-1].content
        return {"research_notes": str(notes)}

    def summarizer_node(state: AgentState) -> AgentState:
        result = summarizer.invoke({
            "messages": [HumanMessage(
                content=f"Ringkas notes berikut jadi 3 bullet point: {state['research_notes']}"
            )]
        })
        return {"summary": str(result["messages"][-1].content)}

    def finish_node(state: AgentState) -> AgentState:
        return {"messages": [HumanMessage(content=state.get("summary", "(kosong)"))]}

    builder = StateGraph(AgentState)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("summarizer", summarizer_node)
    builder.add_node("finish", finish_node)
    builder.add_edge("researcher", "supervisor")
    builder.add_edge("summarizer", "supervisor")
    builder.add_edge("finish", END)
    builder.set_entry_point("supervisor")
    return builder.compile()


def run_supervisor(query: str = "Apa tren multi-agent systems 2026?"):
    """Jalankan supervisor workflow, return summary."""
    graph = build_graph()
    result = graph.invoke({
        "query": query,
        "messages": [],
        "research_notes": "",
        "summary": "",
        "iterations": 0,
    })
    return result.get("summary", "(tidak ada summary)"), result.get("iterations", 0)


if __name__ == "__main__":
    summary, iters = run_supervisor()
    print("=" * 50)
    print("FINAL SUMMARY:")
    print("=" * 50)
    print(summary)
    print(f"\n[debug] iterations dipakai: {iters}")
