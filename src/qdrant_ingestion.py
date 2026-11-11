
import os
import uuid

from qdrant_client import QdrantClient, models

from src.chunking import extract_text_from_pdf, chunk_text
from src.embeddings import generate_embeddings


def ingest_pdf(pdf_path: str):

    # Qdrant configuration from environment variables
    qdrant_url = os.environ["QDRANT_URL"]
    qdrant_api_key = os.environ["QDRANT_API_KEY"]
    collection_name = os.environ["QDRANT_COLLECTION_NAME"]

    # Connect to Qdrant Cloud
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )

    # Step 1: Extract PDF text
    print("Extracting text from PDF...")

    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        raise ValueError("No text extracted from PDF")

    # Step 2: Split text into chunks
    print("Creating chunks...")

    chunks = chunk_text(
        text=text,
        chunk_size=500,
        chunk_overlap=100
    )

    print(f"Total chunks created: {len(chunks)}")

    if not chunks:
        raise ValueError("No chunks created")

    # Step 3: Generate embeddings
    print("Generating embeddings...")

    embeddings = generate_embeddings(chunks)

    # Step 4: Remove old chunks for this PDF
    source = os.path.basename(pdf_path)

    print("Deleting old vectors for this source...")

    client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="source",
                        match=models.MatchValue(value=source)
                    )
                ]
            )
        ),
        wait=True
    )

    # Step 5: Prepare Qdrant points
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

    # Step 6: Upload vectors to Qdrant
    print("Uploading vectors to Qdrant...")

    client.upload_points(
        collection_name=collection_name,
        points=points,
        batch_size=100,
        wait=True
    )

    print("RAG ingestion completed successfully!")

    print(f"PDF: {source}")
    print(f"Chunks uploaded: {len(points)}")
    print(f"Collection: {collection_name}")

    client.close()
