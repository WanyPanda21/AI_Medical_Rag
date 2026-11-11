
from src.qdrant_ingestion import ingest_pdf


def main():

    pdf_path = "data/diseases_symptoms_medicines.pdf"

    ingest_pdf(pdf_path)


if __name__ == "__main__":
    main()
