
import os
import uuid

from qdrant_client import QdrantClient, models
from src.embeddings import generate_embeddings


# Configuration
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "AI_Medicine")
VECTOR_SIZE = 384
BATCH_SIZE = 64

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL:
    raise ValueError("QDRANT_URL is missing")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is missing")


# Qdrant connection
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=120
)

print("Connected to Qdrant Cloud")
print(f"Collection: {COLLECTION_NAME}")


# Step 1: Create or validate collection
def create_collection():

    if not client.collection_exists(COLLECTION_NAME):

        print("Creating Qdrant collection...")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

        print("Collection created successfully.")

    else:

        print("Collection already exists.")

        info = client.get_collection(COLLECTION_NAME)
        config = info.config.params.vectors

        if isinstance(config, dict):
            config = config.get("")

        if config is None or config.size != VECTOR_SIZE:
            raise ValueError(
                "Qdrant collection must support "
                f"{VECTOR_SIZE}-dimensional vectors."
            )

        if config.distance != models.Distance.COSINE:
            raise ValueError(
                "Qdrant collection must use COSINE distance."
            )


# Step 2: Ingest chunks
def ingest_chunks(chunks):

    if not chunks:
        raise ValueError("No chunks available for ingestion.")

    create_collection()

    total_chunks = len(chunks)

    print(f"Total chunks to upload: {total_chunks}")

    # Process in batches
    for start in range(0, total_chunks, BATCH_SIZE):

        batch = chunks[start:start + BATCH_SIZE]

        texts = [
            item["text"]
            for item in batch
        ]

        print(
            f"Generating embeddings for batch "
            f"{start // BATCH_SIZE + 1}"
        )

        vectors = generate_embeddings(texts)

        points = []

        for index, item in enumerate(batch):

            unique_text = (
                f"{item['page']}:"
                f"{item['chunk_index']}:"
                f"{item['text']}"
            )

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    unique_text
                )
            )

            payload = {
                "text": item["text"],
                "page": item["page"],
                "chunk_index": item["chunk_index"],
                "source": "diseases_symptoms_medicines.pdf",
                "document_type": "medical_educational_reference"
            }

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vectors[index],
                    payload=payload
                )
            )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True
        )

        uploaded = min(start + len(batch), total_chunks)

        print(
            f"Successfully uploaded "
            f"{uploaded}/{total_chunks} chunks"
        )

    # Step 3: Verify upload
    collection_info = client.get_collection(
        COLLECTION_NAME
    )

    print("\nQDRANT INGESTION COMPLETED")

    print(
        "Total points in collection:",
        collection_info.points_count
    )

    print(
        "Collection status:",
        collection_info.status
    )

    return collection_info.points_count
