from pydantic import BaseModel
from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from app.services.llm_service import generate_response, generate_streaming_response

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}



class ChatRequest(BaseModel):
    message:str
    history:list[dict] = []
class ChatResponse(BaseModel):
    response:str
    history:list[dict] = []



@router.post("/chat",response_model=ChatResponse)

def chat(request:ChatRequest):
    try:
        response = generate_response(request.message, request.history)
        updated_history = request.history + [{"role": "user", "content": request.message}, {"role": "assistant", "content": response}]

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return ChatResponse(response=response, history=updated_history)

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    """
    Streaming endpoint — returns tokens one by one as Claude generates them.
    StreamingResponse keeps the HTTP connection open and sends chunks.
    media_type tells the client this is an SSE stream, not regular JSON.
    """
    try:
        return StreamingResponse(
            generate_streaming_response(request.message, request.history),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
