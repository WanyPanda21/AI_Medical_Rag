
from src.retrieval import retrieve_documents


# Test query
query = "What are the symptoms of diabetes?"


# Retrieve relevant chunks
results = retrieve_documents(
    query=query,
    top_k=5
)


# Display results
print("\n========== SEARCH RESULTS ==========")

for i, doc in enumerate(results, start=1):

    print(f"\nResult {i}")

    print("Source:", doc["source"])
    print("Chunk Index:", doc["chunk_index"])
    print("Score:", doc["score"])

    print("\nRetrieved Text:")
    print(doc["text"])

    print("-" * 60)
