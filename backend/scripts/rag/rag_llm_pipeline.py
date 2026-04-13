import pickle
import faiss 
import numpy as np

from backend.scripts.rag.embeddings import EmbeddingModel
from backend.scripts.llm.llm_engine import LLMEngine

# Load FAISS + DOCUMENTS

index=faiss.read_index(r"D:\Projects\CHAITRA\scripts\rag\faiss_index.bin")

with open(r"D:\Projects\CHAITRA\scripts\rag\documents.pkl","rb") as f:
    documents=pickle.load(f)

print("FAISS Index + Documents loaded.")

# Load Models

embedding_model=EmbeddingModel()
llm=LLMEngine()

# Retrieval Function

def retrieve_context(query,top_k=5):
    query_embedding=embedding_model.encode([query])

    distances,indices=index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results=[documents[i] for i in indices[0]]
    return "\n\n".join(results)

# RAG Pipeline

def rag_query(query):
    context=retrieve_context(query)

    print("\n Retrieved Context:\n")
    print(context[:500]) 

    response=llm.generate_rag_response(context, query)
    return response

# Test
 
if __name__=="__main__":
    user_query="Why did store 1 sales increase during holidays?"

    answer=rag_query(user_query)

    print("\n Final Answer:\n")
    print(answer)