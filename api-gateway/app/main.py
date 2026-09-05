from fastapi import FastAPI
from pydantic import BaseModel

from app.security.prompt_injection import detect_prompt_injection


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

    if detect_prompt_injection(request.message):
        return {
            "status": "blocked",
            "reason": "Potential prompt injection detected",
            "message": "Request blocked by SecureLLM Security Gateway"
        }

    return {
        "status": "allowed",
        "message": request.message
    }