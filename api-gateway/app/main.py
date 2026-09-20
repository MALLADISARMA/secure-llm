import os

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.history import HistoryService
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


history_service = HistoryService(
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10_000)


def get_session_id(x_session_id: str | None) -> str:
    if not x_session_id:
        raise HTTPException(
            status_code=400,
            detail="X-Session-ID header is required",
        )

    try:
        return HistoryService.validate_session_id(x_session_id)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID",
        ) from error


@app.get("/")
def home():
    return {
        "service": "SecureLLM API Gateway",
        "status": "running",
        "version": "0.1.0"
    }


@app.post("/chat")
def chat(
    request: ChatRequest,
    x_session_id: str | None = Header(default=None),
):
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="message must not be blank")

    session_id = get_session_id(x_session_id)
    analysis = analyze_prompt(request.message)

    if analysis["blocked"]:
        response = {
            "status": "blocked",
            "reason": "Potentially unsafe content detected",
            "message": "Request blocked by SecureLLM Security Gateway",
            "analysis": analysis,
        }

        history_service.save(
            session_id=session_id,
            prompt=request.message,
            status="blocked",
            analysis=analysis,
        )

        return response

    response = {
        "status": "allowed",
        "message": request.message,
        "analysis": analysis,
    }

    history_service.save(
        session_id=session_id,
        prompt=request.message,
        status="allowed",
        analysis=analysis,
    )

    return response


@app.get("/history")
def get_history(x_session_id: str | None = Header(default=None)):
    session_id = get_session_id(x_session_id)
    records = history_service.get(session_id)

    if records is None:
        return {
            "status": "unavailable",
            "records": [],
            "count": 0,
            "message": "History storage is currently unavailable",
        }

    return {
        "status": "success",
        "records": records,
        "count": len(records),
    }


@app.delete("/history")
def clear_history(x_session_id: str | None = Header(default=None)):
    session_id = get_session_id(x_session_id)
    deleted = history_service.delete(session_id)

    if deleted is None:
        return {
            "status": "unavailable",
            "message": "History storage is currently unavailable",
        }

    return {
        "status": "success",
        "message": "History cleared successfully",
    }