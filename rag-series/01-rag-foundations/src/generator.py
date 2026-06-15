# src/generator.py
# Augment + Generate stages.
# Builds an augmented prompt from retrieved chunks and calls the LLM.
#
# Design decisions embedded in this module:
#   1. Empty-chunk check comes FIRST: refuse without calling the LLM at all
#      (cheaper, faster, impossible to hallucinate).
#   2. Every context block carries source name and relevance score: audit trail.
#   3. temperature=0.0: factual Q&A wants determinism, not creativity.
#   4. Two refusal layers: retriever threshold (architectural) +
#      system prompt instruction (behavioral). Either alone fails sometimes;
#      together they fail rarely.
from _shared.llm_client import chat

FALLBACK = "I don't have information on that. Please contact 11111-222."

SYSTEM_INSTRUCTIONS = """
You are a banking assistant. Answer the user's question based ONLY on the
provided context documents. If the answer is not present in the context,
respond with: "I don't have information on that. Please contact 11111-222."

Do not use any knowledge outside the provided context.
""".strip()

PROMPT_TEMPLATE = """
CONTEXT:
{context}

QUESTION: {question}
""".strip()


def build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context block with source citations."""
    blocks = []
    for c in chunks:
        source = c["metadata"]["source"]
        blocks.append(
            f"--- Source: {source} (relevance: {c['score']:.2f}) ---\n{c['content']}"
        )
    return "\n\n".join(blocks)


def generate(question: str, chunks: list[dict]) -> str:
    """Generate a grounded answer from retrieved chunks.

    Returns FALLBACK immediately if no chunks were retrieved,
    without consuming any LLM tokens.
    """
    if not chunks:
        return FALLBACK
    prompt = PROMPT_TEMPLATE.format(
        context=build_context(chunks),
        question=question,
    )
    return chat(SYSTEM_INSTRUCTIONS, prompt, temperature=0.0)
