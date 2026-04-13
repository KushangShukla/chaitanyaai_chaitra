import os
import faiss
import numpy as np
import pickle

from backend.scripts.rag.rag_pipeline import load_data, row_to_text
from backend.scripts.rag.embeddings import EmbeddingModel

# Step 1: Load Data

df=load_data()

with open("scripts/rag/merged_knowledge.pkl","rb") as f:
    documents=pickle.load(f)

print(f"Total documents: {len(documents)}")

# Step 2: Embeddings

print("Generating embeddings...")
model=EmbeddingModel()
embeddings=model.encode(documents)

embeddings=np.array(embeddings).astype("float32")

# Step 3: Faiss Index

dimension=embeddings.shape[1]
index=faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS index created.")

# Save Index

faiss.write_index(index, "faiss_index.bin")

# Save documents

import pickle
with open("documents.pkl","wb") as f:
    pickle.dump(documents,f)

print("Index + documents saved.")

# Step 4: Query Test

query="Why did sales increase in store 1?"

query_embedding=model.encode([query])
query_embedding=np.array(query_embedding).astype("float32")

k=3
distances,indices=index.search(query_embedding,k)

print("\nTop Results:\n")

for i in indices[0]:
    print(documents[i])
    print("-" * 50)