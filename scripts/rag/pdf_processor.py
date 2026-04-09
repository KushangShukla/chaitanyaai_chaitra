import os 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

DB_PATH="vector_store" 

class PDFProcessor:

    def __init__(self):
        self.embedding=HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def process_pdf(self,file_path):

        # 1. Load PDF
        loader=PyPDFLoader(file_path)
        documents=loader.load()

        # 2. Split into chunks
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        docs=splitter.split_documents(documents)

        # 3. Create FAISS DB
        db=FAISS.from_documents(docs,self.embedding)

        # 4. Save Locality
        db.save_local(DB_PATH)

        return f"PDF processed and stored in FAISS with {len(docs)} chunks"