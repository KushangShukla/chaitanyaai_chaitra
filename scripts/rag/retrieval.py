import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from scripts.rag.query_parser import extract_store

from langchain_community.vectorstores import FAISS as LangFAISS
from langchain_huggingface import HuggingFaceEmbeddings

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS Index
index=faiss.read_index("D:/Projects/CHAITRA/scripts/rag/faiss_index.bin")

with open("D:/Projects/CHAITRA/scripts/rag/merged_knowledge.pkl","rb") as f:
    documents=pickle.load(f)

# LANGCHAIN Setup
DB_PATH="vector_store"

embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def clean_context(results):
    seen=[]
    cleaned=[]

    for r in results:
        r=r.strip()

        if r not in seen and len(r)>30:

            seen.add(r)
            cleaned.append(r)

    return "\n\n".join(cleaned[:5])

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

        return clean_context(results)

    base_context= "\n\n".join(results)

    # PDF RAG with LangChain FAISS
    try:
        db=LangFAISS.load_local(
            DB_PATH,
            embedding,
            allow_dangeorus_diserialization=True
        )

        docs=db.similarity_search(query,k=3)

        pdf_context="\n\n".join([d.page_content for d in docs])

        # Merge Both Contexts
        return base_context + "\n\n--- PDF CONTEXT ---\n\n" +pdf_context
    
    except Exception as e:
        # If no PDF uploaded yet then ignore
        return base_context
    
    # Pure PDF Retrieval 
def retrieve_pdf_only(query,k=3):
    try:
        db=LangFAISS.load_local(
            DB_PATH,
            embedding,
            allow_dangerous_diserialization=True
        )

        docs=db.similarity_search(query,k=k)

        return "\n".join([d.page_content for d in docs])
    
    except Exception as e:
        return "No PDF RAG data available"