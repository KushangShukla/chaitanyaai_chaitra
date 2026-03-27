from sentence_transformers import SentenceTransformer
from functools import lru_cache

class EmbeddingModel:
    def __init__(self):
        self.model=SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self,texts):
        return self.model.encode(texts)
    
@lru_cache(maxsize=1000)
def embed_query(query):
    return model.encode([query])