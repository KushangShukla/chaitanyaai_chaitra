import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from scripts.rag.query_parser import extract_store

from langchain.vectorstores import FAISS as LangFAISS
from langchain.embeddings import HuggingFaceEmbeddings

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS Index
index=faiss.read_index("D:/Projects/CHAITRA/scripts/rag/faiss_index.bin")

with open("D:/Projects/CHAITRA/scripts/rag/merged_knowledge.pkl","rb") as f:
    documents=pickle.load(f)

# LANGCHAIN Setup
DB_PATH="vector_store"

embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def retrieve_context(query,top_k=5):
    query_embedding=model.encode([query])
    distances,indices=index.search(np.array(query_embedding),top_k)

    store_number=extract_store(query)

    results=[]

    for i in indices[0]:
        doc=documents[i]

        # Optional Filter
        if store_number:
            if f"Store {store_number}" not in doc:
                continue

        results.append(doc)
    
    # If filtered empty-> fallback to original
    if len(results)==0:
        results=[documents[i] for i in indices[0]]

    base_context= "\n\n".join(results)

    # PDF RAG with LangChain FAISS
    try:
        db=LangFAISS.load_local(
            DB_PATH,
            embedding,
            allow_dangeorus_diserialization=True
        )

        docs=db.similarity_search