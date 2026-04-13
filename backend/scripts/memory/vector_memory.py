import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class VectorMemory:

    def __init__(self):
        self.model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        self.index_path="scripts/memory/chat_memory.index"
        self.data_path="scripts/memory/chat_memory.pkl"

        self.dimension=384

        try:
            self.index=faiss.read_index(self.index_path)
            with open(self.data_path,"rb") as f:
                self.data=pickle.load(f)

        except:
            self.index=faiss.IndexFlatL2(self.dimension)
            self.data=[]

    def add_memory(self,query,response):
        text=query +" " + response
        embedding=self.model.encode([text])

        self.index.add(np.array(embedding))
        self.data.append(text)

        faiss.write_index(self.index,self.index_path)

        with open(self.data_path,"wb") as f:
            pickle.dump(self.data,f)
            
    def search_memory(self,query,top_k=3):
        if len(self.data)==0:
            return ""

        embedding=self.model.encode([query])

        distances,indices=self.index.search(np.array(embedding),top_k)

        results=[]

        for i in indices[0]:
            if i !=-1 and i<len(self.data):
                results.append(self.data[i])
            
        return "\n".join(results)