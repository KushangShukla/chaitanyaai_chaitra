import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from scripts.rag.query_parser import extract_store

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS Index
index=faiss.read_index("D:/Projects/CHAITRA/scripts/rag/faiss_index.bin")

with open("D:/Projects/CHAITRA/scripts/rag/merged_knowledge.pkl","rb") as f:
    documents=pickle.load(f)

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
    
    if len(results)==0:
        results=[documents[i] for i in indices[0]]

    return "\n\n".join(results)