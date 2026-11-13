
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = None


def get_model():

    global model

    if model is None:
        model = SentenceTransformer(
            MODEL_NAME,
            backend="onnx",
            model_kwargs={
                "file_name": "onnx/model_O4.onnx"
            }
        )

    return model


def generate_embeddings(texts: list[str]) -> list[list[float]]:

    if not texts:
        return []

    embedding_model = get_model()

    embeddings = embedding_model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True
    )

    return embeddings.tolist()
