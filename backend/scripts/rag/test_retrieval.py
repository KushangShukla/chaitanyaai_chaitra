from backend.scripts.rag.embeddings import EmbeddingModel
from backend.scripts.rag.vector_store import VectorStore

#Initialize
embedder=EmbeddingModel()

#Sample business knowledge (replace later with ML outputs)
documents=[
    "Q4 revenue increased by 15% due to holiday sales",
    "Customer churn decreased due to improved service",
    "Sales growth driven by discounts and promotions",
    "Unemployment rate impacted purchasing behavior"
]

#Encode
embeddings=embedder.encode(documents)

#Create vector DB
vector_db=VectorStore(dimension=len(embeddings[0]))

#Store data
vector_db.add(embeddings,documents)

#Query
query="Why did revenue increase?"
query_embedding=embedder.encode([query])[0]

#Retrieve
results=vector_db.search(query_embedding)

print("\nTop Relevant Context:\n")
for r in results:
    print("-", r)