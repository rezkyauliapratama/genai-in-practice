# src/qdrant_store.py
# Component #3 (Qdrant version) - same interface as InMemoryVectorStore.
# Exposes: upsert_documents() and similarity_search()
# The pipeline swaps this in with ONE line change.
#
# Key additions over the in-memory store:
#   - Persistence: index survives restarts; re-ingestion UPDATEs, not duplicates
#   - Scale: Qdrant uses HNSW ANN indexes; millisecond search at millions of vectors
#   - Filtering: payload filter (e.g. source="compliance.md") enforced at DB level
#
# Requires Qdrant running locally:
#   docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)


class QdrantVectorStore:
    """Qdrant-backed vector store. Drop-in replacement for InMemoryVectorStore."""

    def __init__(
        self,
        collection: str = "rag_foundations",
        host: str = "localhost",
        port: int = 6333,
        dim: int = 384,          # must match the embedding model dimension
    ):
        self._client = QdrantClient(host=host, port=port)
        self._collection = collection
        if not self._client.collection_exists(collection):
            self._client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert_documents(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        """Upsert chunks into Qdrant.

        Point IDs are derived deterministically from doc_id via uuid5.
        Re-ingesting the same document UPDATE the existing point; no duplicates.
        This is idempotent ingestion without extra bookkeeping.
        """
        points = [
            PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, chunk["doc_id"])),
                vector=embedding,
                payload={"content": chunk["content"], **chunk["metadata"]},
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]
        self._client.upsert(collection_name=self._collection, points=points)

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        source: str | None = None,   # metadata filter: restrict to one document
    ) -> list[dict]:
        """Return top_k results. Optional source filter enforces knowledge-base scoping.

        Example - compliance desk, hard-scoped to approved documents:
            store.similarity_search(query_vec, top_k=5, source="compliance.md")
        """
        query_filter = None
        if source:
            query_filter = Filter(
                must=[FieldCondition(key="source", match=MatchValue(value=source))]
            )
        hits = self._client.query_points(
            collection_name=self._collection,
            query=query_embedding,
            limit=top_k,
            query_filter=query_filter,
        ).points
        return [
            {
                "content": hit.payload["content"],
                "metadata": {k: v for k, v in hit.payload.items() if k != "content"},
                "score": hit.score,
            }
            for hit in hits
        ]
