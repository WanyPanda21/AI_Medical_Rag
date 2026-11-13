
from pypdf import PdfReader



def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file.
    """

    reader = PdfReader(pdf_path)

    extracted_text = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[str]:
    """
    Split text into chunks with overlap.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be non-negative and smaller than chunk size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks
