from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True)
