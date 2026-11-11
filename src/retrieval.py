
import os

from qdrant_client import QdrantClient
from src.embeddings import generate_embeddings


# Configuration
COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "AI_Medicine"
)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


if not QDRANT_URL:
    raise ValueError("QDRANT_URL is missing")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is missing")


# Connect to Qdrant Cloud
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=120
)


print("Connected to Qdrant Cloud")


def retrieve_documents(
    query,
    top_k=5
):

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    print("\nUser Query:", query)

    # Step 1: Generate query embedding
    print("\nGenerating query embedding...")

    query_vector = generate_embeddings([query])[0]

    print(
        "Query embedding generated.",
        "Vector dimensions:",
        len(query_vector)
    )

    # Step 2: Search Qdrant
    print("\nSearching Qdrant...")

    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    ).points

    # Step 3: Extract retrieved information
    retrieved_documents = []

    for result in search_results:

        payload = result.payload or {}

        retrieved_documents.append({

            "text": payload.get("text", ""),

            "page": payload.get("page"),

            "chunk_index": payload.get("chunk_index"),

            "source": payload.get("source"),

            "score": result.score

        })

    print(
        f"\nRetrieved {len(retrieved_documents)} documents."
    )

    return retrieved_documents
