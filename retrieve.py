
from src.retrieval import retrieve_documents


def main():

    print("=" * 60)
    print("MEDICAL RAG - RETRIEVAL PHASE")
    print("=" * 60)

    # User question
    query = input("\nEnter your medical question: ")

    # Retrieve relevant documents
    results = retrieve_documents(
        query=query,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("RETRIEVED MEDICAL INFORMATION")
    print("=" * 60)

    for index, document in enumerate(results, 1):

        print(f"\nDocument {index}")

        print("-" * 60)

        print("Similarity Score:", document["score"])

        print("Page:", document["page"])

        print("Chunk:", document["chunk_index"])

        print("\nText:")

        print(document["text"])

    print("\n" + "=" * 60)
    print("RETRIEVAL COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
