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
    user_id = request.user_id or "default_user"
    chat_mode = request.chat_mode or "auto"

    # Keep default path responsive for UI while heavy models run.
    if request.fast_mode and len(user_query.split()) <= 6 and "predict" not in user_query.lower() and chat_mode == "auto":
        response = "📊 Key Insight:\nYour query is received.\n\n📈 Recommendation:\nUse a detailed question for deeper analysis.\n\n⚠️ Risk:\nShort prompts may return generic insights."
        query_router.memory.save_chat(user_id, "user", user_query, response)
    else:
        mode_override = None if chat_mode == "auto" else chat_mode
        response=query_router.route(user_query, user_id=user_id, mode_override=mode_override)
    return {
        "query":user_query,
        "user_id": user_id,
        "response":response,
        "source":"rag" if "why" in user_query.lower() else "llm",
        "status":"success"
    }