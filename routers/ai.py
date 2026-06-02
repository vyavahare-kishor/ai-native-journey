from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.ai import chat, stream_chat

router = APIRouter(prefix="/ai", tags=["AI"])

# --- Schemas ---


class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    system: str | None = None
    stream: bool = False


class ChatResponse(BaseModel):
    reply: str


# --- Basic Chat Endpoint ---
@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    messages = [m.model_dump() for m in request.messages]
    reply = chat(messages, system=request.system)
    return {"reply": reply}


# --- Streaming Chat Endpoint ---
@router.post("/chat/stream")
def stream_chat_endpoint(request: ChatRequest):
    messages = [m.model_dump() for m in request.messages]

    def generate():
        for chunk in stream_chat(messages, system=request.system):
            # SSE format — you learned this!
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
