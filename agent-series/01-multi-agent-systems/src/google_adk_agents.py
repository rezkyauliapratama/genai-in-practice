"""Task 3 — Google ADK Quickstart (single + multi-agent).

Root agent (koordinator) + 2 sub-agents (researcher, summarizer).
Model via litellm: deepseek/deepseek-chat (pakai DEEPSEEK_API_KEY env).
Catatan API ADK >= 2.7:
- function_tool bukan decorator -> FunctionTool(func=...)
- Runner.run = generator events + new_message=Content(parts=[...])
- create_session async -> asyncio.run(...)
- model provider-style butuh pip install litellm
"""
import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.genai import types

from .config import DEEPSEEK_API_KEY, DEEPSEEK_CHAT_MODEL, check_env

load_dotenv()

MODEL = f"deepseek/{DEEPSEEK_CHAT_MODEL}"


# --- Function tool (dummy untuk tes) ---
def web_search_tool(query: str) -> str:
    """Cari info di web (dummy untuk tes)."""
    return (
        f"Hasil pencarian untuk '{query}': "
        "Agentic AI 2026 didominasi orchestrator patterns, "
        "standar MCP + A2A, adopsi enterprise ~40%."
    )


web_search_tool = FunctionTool(func=web_search_tool)


def build_agents():
    """Bangun root + sub-agents."""
    check_env()
    research_agent = Agent(
        name="researcher",
        model=MODEL,
        instruction="Kamu peneliti. Cari fakta, jawab dengan sumber. Gunakan web_search_tool.",
        tools=[web_search_tool],
        description="Meneliti topik dan mengumpulkan fakta",
    )
    summary_agent = Agent(
        name="summarizer",
        model=MODEL,
        instruction="Kamu perangkum. Ringkas informasi jadi maksimal 3 bullet point.",
        description="Meringkas informasi",
    )
    root_agent = Agent(
        name="root",
        model=MODEL,
        instruction="""
        Kamu koordinator multi-agent.
        Untuk pertanyaan riset, delegasikan ke researcher.
        Untuk peringkasan, delegasikan ke summarizer.
        """,
        sub_agents=[research_agent, summary_agent],
        description="Koordinator multi-agent",
    )
    return root_agent


def run_query(root_agent: Agent, message: str) -> str:
    """Jalankan 1 query ke root agent, return teks final."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="my_app",
        session_service=session_service,
    )
    asyncio.run(session_service.create_session(
        app_name="my_app", user_id="user1", session_id="s1"
    ))
    events = list(runner.run(
        user_id="user1", session_id="s1",
        new_message=types.Content(parts=[types.Part(text=message)]),
    ))
    for ev in reversed(events):
        if ev.content and ev.content.parts:
            texts = [p.text for p in ev.content.parts if p.text]
            if texts:
                return "\n".join(texts)
    return "(tidak ada output)"


def run_adk():
    """Jalankan 2 tes delegasi: research + summarize."""
    root = build_agents()
    print("TEST 1 — research delegation:")
    print(run_query(root, "Riset tren agentic AI 2026"))
    print()
    print("TEST 2 — summarize delegation:")
    print(run_query(
        root,
        "Ringkas ini: MCP adalah protokol untuk tools, A2A untuk antar-agent. "
        "Keduanya saling melengkapi dan diadopsi OpenAI, Google, dan Microsoft.",
    ))


if __name__ == "__main__":
    run_adk()
