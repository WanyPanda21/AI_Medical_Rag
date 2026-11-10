
import os

from src.disease_data import DISEASES
from src.generate_pdf import generate_pdf
from src.chunking import create_document_chunks
from src.qdrant_ingestion import ingest_chunks


def main():

    print("=" * 60)
    print("MEDICAL RAG - PDF TO QDRANT INGESTION")
    print("=" * 60)

    # Step 1: Validate dataset
    print("\nStep 1: Validating disease dataset...")

    if len(DISEASES) != 50:
        raise ValueError(
            f"Expected 50 diseases, found {len(DISEASES)}"
        )

    print(f"Validated {len(DISEASES)} diseases.")

    # Step 2: Generate PDF
    print("\nStep 2: Generating PDF...")

    pdf_path = generate_pdf()

    # Step 3: Extract and chunk PDF
    print("\nStep 3: Extracting and chunking PDF...")

    chunks = create_document_chunks(pdf_path)

    if not chunks:
        raise ValueError("No text chunks extracted from PDF.")

    # Step 4: Inject into Qdrant
    print("\nStep 4: Injecting embeddings into Qdrant...")

    ingest_chunks(chunks)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"PDF: {pdf_path}")
    print(f"Diseases: {len(DISEASES)}")
    print(f"Chunks: {len(chunks)}")


if __name__ == "__main__":

    required_variables = [
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "COLLECTION_NAME"
    ]

    for variable in required_variables:

        if not os.getenv(variable):
            raise EnvironmentError(
                f"Missing environment variable: {variable}"
            )

    main()
