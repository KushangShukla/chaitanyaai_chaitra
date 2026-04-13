from fastapi import APIRouter,UploadFile,File
import os
from backend.rag.pdf_processor import PDFProcessor

router=APIRouter()

UPLOAD_DIR="pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

processor=PDFProcessor()

@router.post("/upload-pdf")
async def upload_pdf(file:UploadFile=File(...)):
    try:
        file_path=os.path.join(UPLOAD_DIR,file.filename)

        with open(file_path,"wb") as f:
            f.write(await file.read())

        result=processor.process_pdf(file_path)

        return{"status":"success","message":result}
    
    except Exception as e:
        return {"error":str(e)}
    