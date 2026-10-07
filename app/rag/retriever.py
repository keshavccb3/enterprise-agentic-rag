import numpy as np
import faiss
from app.core.config import settings
from app.rag.embeddings import EmbeddingModel
from app.rag.loader import read_documents, chunk_text

class VectorRetriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.index = None
        self.records = []

    def rebuild(self, directory=None):
        records = []
        for doc in read_documents(directory):
            for number, chunk in enumerate(chunk_text(doc["text"], settings.chunk_size, settings.chunk_overlap)):
                records.append({"source": doc["source"], "chunk": number, "text": chunk})
        self.records = records
        if not records:
            self.index = None
            return 0
        vectors = np.asarray(self.embedder.encode([r["text"] for r in records]), dtype="float32")
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)
        return len(records)

    def search(self, query, top_k=4):
        if self.index is None or not self.records:
            return []
        vector = np.asarray(self.embedder.encode([query]), dtype="float32")
        scores, ids = self.index.search(vector, min(top_k, len(self.records)))
        return [{**self.records[i], "score": round(float(s), 4)} for s, i in zip(scores[0], ids[0]) if i >= 0]
