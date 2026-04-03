from fastapi import FastAPI
from backend.routes.query import router as query_router
from backend.routes.predict import router as predict_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="CHAITRA AI API")

app.include_router(query_router)
app.include_router(predict_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message":"CHAITRA API is running"}