
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None


def get_model():
    """
    Load the ONNX embedding model only when required.
    """

    global _model

    if _model is None:

        _model = SentenceTransformer(
            MODEL_NAME,
            backend="onnx",
            model_kwargs={
                "file_name": "onnx/model_O4.onnx"
            }
        )

    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate normalized ONNX embeddings.
    """

    if not texts:
        return []

    model = get_model()

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    return embeddings.tolist()
