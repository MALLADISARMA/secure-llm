import requests
import os


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434/api/generate",
)

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


def generate_response(prompt: str) -> str:

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    if (
        response.status_code == 500
        and "out of memory" in response.text.lower()
    ):
        payload["options"] = {"num_gpu": 0}
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

    response.raise_for_status()

    data = response.json()

    return data["response"]