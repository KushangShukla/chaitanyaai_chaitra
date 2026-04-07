from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    user_id: str | None = "default_user"
    fast_mode: bool | None = True
    chat_mode: str | None = "auto"