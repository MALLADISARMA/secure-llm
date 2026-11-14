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
        status_code = 200
        text = ""

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


def test_ollama_service_retries_gpu_out_of_memory_on_cpu(monkeypatch):
    service = load_ollama_service()
    requests_made = []

    class FakeResponse:
        def __init__(self, status_code, text, data):
            self.status_code = status_code
            self.text = text
            self.data = data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise service.requests.HTTPError(response=self)

        def json(self):
            return self.data

    responses = [
        FakeResponse(
            500,
            "CUDA allocation failed: out of memory",
            {"error": "out of memory"},
        ),
        FakeResponse(200, "", {"response": "Generated on CPU"}),
    ]

    def fake_post(url, json, timeout):
        requests_made.append((url, json.copy(), timeout))
        return responses.pop(0)

    monkeypatch.setattr(service.requests, "post", fake_post)

    assert service.generate_response("Explain Kubernetes") == "Generated on CPU"
    assert len(requests_made) == 2
    assert requests_made[0][1] == {
        "model": "qwen2.5:1.5b",
        "prompt": "Explain Kubernetes",
        "stream": False,
    }
    assert requests_made[1][1] == {
        "model": "qwen2.5:1.5b",
        "prompt": "Explain Kubernetes",
        "stream": False,
        "options": {"num_gpu": 0},
    }