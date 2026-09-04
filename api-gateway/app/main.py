from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="SecureLLM API Gateway",
    description="API Gateway with basic LLM security checks",
    version="0.1.0"
)


class ChatRequest(BaseModel):
    message: str


def detect_prompt_injection(message: str) -> bool:
    """
    Basic prompt injection detection.
    This is an initial rule-based implementation.
    """

    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore your instructions",
        "system prompt",
        "reveal your prompt",
        "jailbreak"
    ]

    message = message.lower()

    for pattern in suspicious_patterns:
        if pattern in message:
            return True

    return False


@app.get("/")
def home():
    return {
        "service": "SecureLLM API Gateway",
        "status": "running",
        "version": "0.1.0"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Security check
    is_attack = detect_prompt_injection(request.message)

    if is_attack:
        return {
            "status": "blocked",
            "reason": "Potential prompt injection detected",
            "message": "Request blocked by SecureLLM Security Gateway"
        }

    # For now, we simply allow the request.
    # Later this request will be sent to vLLM.
    return {
        "status": "allowed",
        "message": request.message
    }