from fastapi import APIRouter
from backend.schemas.request import QueryRequest

# Import Existing System
from scripts.orchestrator.query_router import QueryRouter

router=APIRouter()

# Initialize once
query_router=QueryRouter()

@router.post("/query")
def handle_query(request:QueryRequest):
    
    user_query=request.query

    response=query_router.route(user_query)
    return {
        "query":user_query,
        "response":response,
        "source":"rag" if "why" in user_query.lower() else "llm",
        "status":"success"
    }