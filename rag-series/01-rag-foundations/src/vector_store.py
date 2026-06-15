# src/vector_store.py
# Component #3 (in-memory version) - Vector store built from scratch.
# Purpose: understand exactly what a vector database does before using a real one.
#
# The entire "magic" of semantic search:
#   scores = matrix @ query_vector
# Because vectors are L2-normalised, this dot product == cosine similarity.
# Cosine similarity: 1.0 = same meaning, ~0.0 = unrelated.
#
# Limitation: exact search over every stored vector.
# Fine for hundreds/thousands of chunks; a real DB (see qdrant_store.py) uses
# ANN indexes (HNSW) to scale to millions without degrading latency.
import numpy as np


class InMemoryVectorStore:
    """A list of chunks, a matrix of embeddings, and a dot product. That's it."""

    def __init__(self):
        self._chunks: list[dict] = []
        self._matrix: np.ndarray | None = None

    def upsert_documents(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        """Store chunks and their embeddings, replacing any previous data."""
        self._chunks = chunks
        self._matrix = np.array(embeddings)  # shape: (num_chunks, embedding_dim)

    def similarity_search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """Return top_k chunks sorted by cosine similarity to the query."""
        if self._matrix is None or len(self._chunks) == 0:
            return []
        # Vectors are L2-normalised so dot product == cosine similarity
        scores = self._matrix @ np.array(query_embedding)
        top_idx = np.argsort(scores)[::-1][:top_k]   # highest scores first
        return [
            {
                "content": self._chunks[i]["content"],
                "metadata": self._chunks[i]["metadata"],
                "score": float(scores[i]),
            }
            for i in top_idx
        ]
