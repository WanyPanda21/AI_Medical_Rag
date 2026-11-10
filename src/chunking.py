
import fitz


def extract_pdf_text(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages


def split_into_chunks(
    text,
    chunk_size=800,
    overlap=150
):

    text = " ".join(text.split())

    chunks = []

    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # Prefer ending at a word boundary.
        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def create_document_chunks(pdf_path):

    pages = extract_pdf_text(pdf_path)

    all_chunks = []

    for page in pages:

        chunks = split_into_chunks(page["text"])

        for chunk_index, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "page": page["page"],
                "chunk_index": chunk_index
            })

    print(f"Total chunks generated: {len(all_chunks)}")

    return all_chunks
