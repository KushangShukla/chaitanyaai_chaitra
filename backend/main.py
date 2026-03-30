from fastapi import FastAPI
from backend.routes.query import router as query_router
from backend.routes.predict import router as predict_router

app=FastAPI(title="CHAITRA AI API")

app.include_router(query_router)
app.include_router(predict_router)

@app.get("/")
def home():
    return {"message":"CHAITRA API is running"}