# src/embedder.py
# Component #2 - Embedding model.
# Converts text to dense numerical vectors where distance == semantic similarity.
# Supports local HuggingFace (free, CPU-friendly) and OpenAI API embeddings.
#
# Critical rule: documents and queries MUST use the same model.
# normalize_embeddings=True reduces cosine similarity to a dot product,
# which simplifies the vector store math in the next module.
import sys
from _shared.config import settings


class Embedder:
    """Provider-agnostic text embedder. Switch via EMBEDDING_PROVIDER in .env."""

    def __init__(self):
        self.provider = settings.embedding_provider
        if self.provider == "huggingface":
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        elif self.provider == "openai":
            from openai import OpenAI
            self._client = OpenAI(api_key=settings.openai_api_key)
        else:
            print(f"Unknown embedding provider: {self.provider}", file=sys.stderr)
            raise ValueError(f"Unsupported embedding provider: {self.provider}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts and return a list of float vectors."""
        if self.provider == "huggingface":
            return self._model.encode(texts, normalize_embeddings=True).tolist()
        # OpenAI path
        response = self._client.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )
        return [d.embedding for d in response.data]
