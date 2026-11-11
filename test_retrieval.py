
from src.retrieval import retrieve_documents


def test_retrieval():

    test_queries = [
        "What are the symptoms of Type 2 Diabetes?",
        "What are the symptoms of asthma?",
        "What are the symptoms of dengue?",
        "What are the symptoms of migraine?",
        "What are the symptoms of hypertension?"
    ]

    for query in test_queries:

        print("\n" + "=" * 60)
        print("USER QUERY:", query)
        print("=" * 60)

        results = retrieve_documents(
            query=query,
            top_k=5
        )

        if not results:
            raise AssertionError(
                f"No documents retrieved for: {query}"
            )

        for index, document in enumerate(results, 1):

            print(f"\nRetrieved Document {index}")

            print("Similarity Score:", document["score"])
            print("Page:", document["page"])

            print("\nRetrieved Text:")
            print(document["text"])

    print("\nALL RETRIEVAL TESTS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    test_retrieval()
