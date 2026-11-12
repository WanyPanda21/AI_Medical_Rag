
from src.generator import generate_answer


def main():

    # Ask a question
    query = "What are the symptoms of diabetes?"

    print("\n================================")
    print("       MEDICAL RAG CHATBOT")
    print("================================")

    print("\nUser Question:")
    print(query)

    # Generate answer using Claude
    result = generate_answer(
        query=query,
        top_k=5
    )

    # Display answer
    print("\n========== AI GENERATED ANSWER ==========\n")

    print(result["answer"])

    # Display sources
    print("\n========== RETRIEVED SOURCES ==========\n")

    for source in result["sources"]:

        print("PDF:", source["source"])
        print("Chunk:", source["chunk_index"])
        print("Similarity Score:", source["score"])
        print("--------------------------------")

    print("\n========== COMPLETED ==========")


if __name__ == "__main__":
    main()
