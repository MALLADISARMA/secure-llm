from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.security.analyzer import analyze_prompt


app = FastAPI(
    title="SecureLLM API Gateway",
    description="API Gateway with LLM security checks",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10_000)


@app.get("/")
def home():
    return {
        "service": "SecureLLM API Gateway",
        "status": "running",
        "version": "0.1.0"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="message must not be blank")

    analysis = analyze_prompt(request.message)

    if analysis["blocked"]:
        return {
            "status": "blocked",
            "reason": "Potentially unsafe content detected",
            "message": "Request blocked by SecureLLM Security Gateway",
            "analysis": analysis,
        }

    return {
        "status": "allowed",
        "message": request.message,
        "analysis": analysis,
    }