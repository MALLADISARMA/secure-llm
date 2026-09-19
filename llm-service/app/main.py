from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import ChatRequest, ChatResponse
from app.serviecs.ollama_service import generate_response


app = FastAPI(
    title="SecureLLM Local LLM Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "SecureLLM LLM Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.post(
    "/generate",
    response_model=ChatResponse,
    responses={500: {"description": "LLM generation failed"}},
)
def generate(request: ChatRequest):

    try:
        response = generate_response(request.message)

        return ChatResponse(
            response=response
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM generation failed: {str(e)}"
        )