
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = None


def load_embedding_model():

    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer(MODEL_NAME)

    return model


def generate_embeddings(texts):

    embedding_model = load_embedding_model()

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()
