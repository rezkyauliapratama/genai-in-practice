# src/pipeline.py
# Component #5 - RAGPipeline orchestrator.
# Wires all five components into one cohesive system.
#
# index() = build the library  (load -> chunk -> embed -> store)
# query() = consult the library (retrieve -> augment -> generate)
#
# To swap in Qdrant, change ONE line:
#   from src.qdrant_store import QdrantVectorStore
#   self.store = QdrantVectorStore()
from src.chunker import chunk_documents, load_documents
from src.embedder import Embedder
from src.retriever import Retriever
from src.vector_store import InMemoryVectorStore
from src import generator


class RAGPipeline:
    """End-to-end RAG pipeline."""

    def __init__(self, top_k: int = 5, score_threshold: float = 0.3):
        self.embedder = Embedder()
        self.store = InMemoryVectorStore()
        # To use Qdrant instead (Level Up section):
        # from src.qdrant_store import QdrantVectorStore
        # self.store = QdrantVectorStore()
        self.retriever = Retriever(
            self.embedder,
            self.store,
            top_k=top_k,
            score_threshold=score_threshold,
        )

    def index(self, data_dir: str = "data") -> int:
        """Load -> chunk -> embed -> store. Returns number of chunks indexed."""
        docs = load_documents(data_dir)
        chunks = chunk_documents(docs)
        embeddings = self.embedder.embed([c["content"] for c in chunks])
        self.store.upsert_documents(chunks, embeddings)
        return len(chunks)

    def query(self, question: str) -> str:
        """Retrieve -> Augment -> Generate."""
        chunks = self.retriever.retrieve(question)
        return generator.generate(question, chunks)


if __name__ == "__main__":
    pipeline = RAGPipeline()
    n = pipeline.index()
    print(f"Indexed {n} chunks. RAG pipeline ready. Type 'exit' to quit.\n")

    while True:
        question = input("Your question: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if question:
            print(f"\n{pipeline.query(question)}\n")
