
import os
import uuid

from qdrant_client import QdrantClient, models

from src.chunking import extract_text_from_pdf, chunk_text
from src.embeddings import generate_embeddings


def ingest_pdf(pdf_path: str):

    # Step 1: Get Qdrant configuration

    qdrant_url = os.environ["QDRANT_URL"]
    qdrant_api_key = os.environ["QDRANT_API_KEY"]

    collection_name = os.environ["QDRANT_COLLECTION_NAME"]

    # FIX: Define source filename
    source = os.path.basename(pdf_path)

    # Step 2: Connect to Qdrant Cloud

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=120
    )

    try:

        # Step 3: Extract PDF text

        print("Extracting text from PDF...")

        text = extract_text_from_pdf(pdf_path)

        if not text.strip():
            raise ValueError("No text extracted from PDF")

        # Step 4: Create chunks

        print("Creating chunks...")

        chunks = chunk_text(
            text=text,
            chunk_size=500,
            chunk_overlap=100
        )

        print(f"Total chunks created: {len(chunks)}")

        if not chunks:
            raise ValueError("No chunks created")

        # Step 5: Generate embeddings

        print("Generating embeddings...")

        embeddings = generate_embeddings(chunks)

        if len(embeddings) != len(chunks):
            raise ValueError("Embedding count does not match chunk count")

        # Step 6: Prepare Qdrant points

        points = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{source}_{index}"
                )
            )

            point = models.PointStruct(
                id=point_id,

                vector=embedding,

                payload={
                    "text": chunk,
                    "source": source,
                    "chunk_index": index
                }
            )

            points.append(point)

        # Step 7: Upload vectors to Qdrant

        print("Uploading vectors to Qdrant...")

        client.upload_points(
            collection_name=collection_name,
            points=points,
            batch_size=100,
            wait=True
        )

        print("\nRAG ingestion completed successfully!")

        print(f"PDF: {source}")
        print(f"Chunks uploaded: {len(points)}")
        print(f"Collection: {collection_name}")

    finally:
        client.close()
