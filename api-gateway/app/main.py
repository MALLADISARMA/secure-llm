from fastapi import FastAPI
from pydantic import BaseModel

from app.security.policy import is_unsafe_message


app = FastAPI(
    title="SecureLLM API Gateway",
    description="API Gateway with LLM security checks",
    version="0.1.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "service": "SecureLLM API Gateway",
        "status": "running",
        "version": "0.1.0"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if is_unsafe_message(request.message):
        return {
            "status": "blocked",
            "reason": "Potentially unsafe content detected",
            "message": "Request blocked by SecureLLM Security Gateway"
        }

    return {
        "status": "allowed",
        "message": request.message
    }