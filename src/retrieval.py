import os
from qdrant_client import QdrantClient
from backend.medical_rag.src.embeddings import generate_embeddings

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", os.getenv("QDRANT_COLLECTION_NAME", "medical_knowledge"))
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL:
    raise RuntimeError("QDRANT_URL environment variable is missing")
if not QDRANT_API_KEY:
    raise RuntimeError("QDRANT_API_KEY environment variable is missing")

_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=120)


def retrieve_documents(query: str, top_k: int = 5):
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    if top_k <= 0:
        raise ValueError("top_k must be positive")

    vector = generate_embeddings([query.strip()])[0]
    if len(vector) != 384:
        raise RuntimeError(f"Expected 384 embedding dimensions; got {len(vector)}")

    points = _client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=top_k,
        with_payload=True,
    ).points

    docs = []
    for point in points:
        payload = point.payload or {}
        docs.append({
            "text": payload.get("text", ""),
            "page": payload.get("page"),
            "chunk_index": payload.get("chunk_index"),
            "source": payload.get("source"),
            "score": point.score,
        })
    return docs
