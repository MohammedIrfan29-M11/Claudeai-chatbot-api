from pydantic import  BaseModel, field_validator
from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from app.services.llm_service import generate_response, generate_streaming_response
from app.core.config import MAX_MESSAGE_LENGTH, MIN_MESSAGE_LENGTH, MAX_HISTORY_LENGTH
import logging

logger = logging.getLogger("app.routes")


router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}



class ChatRequest(BaseModel):
    message:str
    history:list[dict] = []

    @field_validator("message")
    @classmethod
    def validate_message_length(cls, value):
        value = value.strip()
        if len(value) < MIN_MESSAGE_LENGTH:
            raise ValueError(f"Message cannot be empty")
        if len(value) > MAX_MESSAGE_LENGTH:
            raise ValueError(
                f"Message too long. Max length is {MAX_MESSAGE_LENGTH} characters."
                f"got {len(value)}"
            )
        value = value.replace('\x00', '')
        return value

    @field_validator("history")
    @classmethod
    def validate_history(cls, value):
        for i, turn in enumerate(value):
            if "role" not in turn or "content" not in turn:
                raise ValueError(
                    f"History item {i} missing 'role' or 'content'"
                )
            if turn["role"] not in ["user", "assistant"]:
                raise ValueError(
                    f"History item {i} has invalid role: {turn['role']}"
                )
        if len(value) > MAX_HISTORY_LENGTH:
            logger.warning(
                f"History too long({len(value)} turns), "
                f"truncating to last {MAX_HISTORY_LENGTH} turns."
            )
        value = value[-MAX_HISTORY_LENGTH:]
    
        return value


class ChatResponse(BaseModel):
    response: str
    history: list[dict] = []

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info(f"POST /chat | message: '{request.message[:50]}...'")
    try:
        response = generate_response(request.message, request.history)
        updated_history = request.history + [{"role": "user", "content": request.message}, {"role": "assistant", "content": response}]      
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return ChatResponse(response=response, history=updated_history)

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    logger.info(f"POST /chat/stream | message: '{request.message[:50]}...'")
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
        logger.error(f"Error in /chat/stream endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
