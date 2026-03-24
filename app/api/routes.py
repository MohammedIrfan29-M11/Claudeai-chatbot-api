from pydantic import BaseModel
from fastapi import APIRouter
from app.services.llm_service import generate_response

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}



class ChatRequest(BaseModel):
    message:str

@router.post("/chat")
def chat(request:ChatRequest):
    ai_response = generate_response(request.message)
    return {"response": ai_response}

