import pickle 

def load_documents():

    with open("scripts/rag/documents.pkl","rb") as f:
        docs1=pickle.load(f)

    with open("scripts/rag/ml_knowledge.pkl","rb") as f:
        docs2=pickle.load(f)

    print("Business documents:",len(docs1))
    print("ML Knowledge docs:", len(docs2))

    return docs1+docs2

def save_merged(docs):
    with open ("scripts/rag/merged_knowledge.pkl","wb") as f:
        pickle.dump(docs,f)

    print("Merged knowledge saved.")

if __name__=="__main__":
    documents=load_documents()
    save_merged(documents)
