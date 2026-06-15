# _shared/llm_client.py
# Provider-agnostic LLM client.
# OpenAI, Gemini, and Groq all expose OpenAI-compatible endpoints,
# so one client library covers all three. Switching provider = one .env change.
from openai import OpenAI
from _shared.config import settings

_PROVIDERS = {
    "openai": dict(
        base_url=None,
        key=settings.openai_api_key,
        model="gpt-4o-mini",
    ),
    "groq": dict(
        base_url="https://api.groq.com/openai/v1",
        key=settings.groq_api_key,
        model="llama-3.1-70b-versatile",
    ),
    "gemini": dict(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        key=settings.gemini_api_key,
        model="gemini-2.0-flash",
    ),
}


def chat(system: str, user: str, temperature: float = 0.0) -> str:
    """Send a chat message to the configured LLM provider and return the response."""
    cfg = _PROVIDERS[settings.llm_provider]
    client = OpenAI(api_key=cfg["key"], base_url=cfg["base_url"])
    response = client.chat.completions.create(
        model=cfg["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content
