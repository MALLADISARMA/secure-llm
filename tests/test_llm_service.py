import importlib.util
from pathlib import Path


LLM_SERVICE_ROOT = Path(__file__).resolve().parents[1] / "llm-service"
OLLAMA_SERVICE_PATH = (
    LLM_SERVICE_ROOT / "app" / "serviecs" / "ollama_service.py"
)


def load_ollama_service():
    spec = importlib.util.spec_from_file_location(
        "securellm_ollama_service",
        OLLAMA_SERVICE_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ollama_service_posts_configured_generation_request(monkeypatch):
    service = load_ollama_service()
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": "Generated response"}

    def fake_post(url, json, timeout):
        captured.update(url=url, json=json, timeout=timeout)
        return FakeResponse()

    monkeypatch.setattr(service.requests, "post", fake_post)

    assert service.generate_response("Explain Kubernetes") == "Generated response"
    assert captured == {
        "url": "http://host.docker.internal:11434/api/generate",
        "json": {
            "model": "qwen2.5:1.5b",
            "prompt": "Explain Kubernetes",
            "stream": False,
        },
        "timeout": 120,
    }