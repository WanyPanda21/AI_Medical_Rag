
import os

from qdrant_client import QdrantClient
from src.embeddings import generate_embeddings


COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "ai_medicine_test"
)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


if not QDRANT_URL:
    raise ValueError("QDRANT_URL is missing")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is missing")


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=120
)


def retrieve_documents(query: str, top_k: int = 5):
    """
    Retrieve relevant documents from Qdrant.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    print("Generating query embedding...")

    query_vector = generate_embeddings([query.strip()])[0]

    if len(query_vector) != 384:
        raise ValueError(
            f"Expected 384 dimensions, got {len(query_vector)}"
        )

    print("Searching Qdrant...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    ).points

    retrieved_documents = []

    for result in results:

        payload = result.payload or {}

        retrieved_documents.append({
            "text": payload.get("text", ""),
            "page": payload.get("page"),
            "chunk_index": payload.get("chunk_index"),
            "source": payload.get("source"),
            "score": result.score
        })

    print(f"Retrieved {len(retrieved_documents)} documents.")

    return retrieved_documents
