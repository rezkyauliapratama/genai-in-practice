# src/retriever.py
# Component #4 - Retriever with relevance gate.
# Embeds the query, runs similarity search, and filters out low-scoring results.
#
# Why a separate module from the vector store?
# Raw similarity search ALWAYS returns top_k results, even when none are relevant.
# The score_threshold is the architectural defense against out-of-scope queries:
# if no chunk clears the bar, an empty list is returned and the generator refuses
# to answer - WITHOUT ever calling the LLM.
#
# Threshold calibration:
#   - MiniLM scores typically run 0.3-0.7 for relevant matches
#   - OpenAI text-embedding-3-small scores run 0.6-0.9 for the same
#   - Calibrate by printing scores for 10 "should match" and 10 "should not" queries
#     and placing the threshold in the gap between the two distributions.
from src.embedder import Embedder


class Retriever:
    """Embed query, search store, filter by score threshold."""

    def __init__(
        self,
        embedder: Embedder,
        store,                          # anything with similarity_search()
        top_k: int = 5,
        score_threshold: float = 0.3,   # model-dependent; calibrate empirically
    ):
        self.embedder = embedder
        self.store = store
        self.top_k = top_k
        self.score_threshold = score_threshold

    def retrieve(self, query: str) -> list[dict]:
        """Return chunks relevant to query, or empty list if nothing clears threshold."""
        query_embedding = self.embedder.embed([query])[0]
        results = self.store.similarity_search(query_embedding, top_k=self.top_k)
        return [r for r in results if r["score"] >= self.score_threshold]
