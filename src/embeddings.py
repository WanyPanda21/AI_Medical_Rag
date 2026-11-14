from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = None


def get_model():
    global _model
    if _model is None:
        # This must be the same model/config used by your GitHub ingestion job.
        _model = SentenceTransformer(
            MODEL_NAME,
            backend="onnx",
            model_kwargs={"file_name": "onnx/model_O4.onnx"},
        )
    return _model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = get_model().encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return vectors.tolist()
