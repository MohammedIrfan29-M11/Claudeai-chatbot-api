from pydantic import BaseModel
from fastapi import APIRouter,HTTPException
from app.services.llm_service import generate_response

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
