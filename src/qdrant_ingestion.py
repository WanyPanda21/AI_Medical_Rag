
import os
import uuid

from qdrant_client import QdrantClient, models

from src.embeddings import generate_embeddings


# Qdrant configuration

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "AI_Medicine"
)

VECTOR_SIZE = 384
BATCH_SIZE = 64

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
print(f"Collection: {COLLECTION_NAME}")
