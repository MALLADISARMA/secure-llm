# SecureLLM

SecureLLM is an open-source prompt security gateway for LLM applications. It analyzes prompts before they reach an optional local language model and returns category-level findings, confidence scores, and an allow-or-block decision.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

## Current Capabilities

- React and Vite interface for submitting prompts and reviewing analysis.
- FastAPI gateway with prompt-injection, jailbreak, sensitive-information, system-prompt-leakage, toxicity, and malicious-intent detectors.
- Risk scoring and policy decisions; a detected category at or above the configured confidence threshold blocks the prompt.
- Optional Redis-backed, session-scoped analysis history.
- Optional Docker-based generation service using Ollama and a locally hosted model.

RAG document scanning, tool authorization, Kubernetes deployment, and other platform controls are future work, not implemented features. Security classifications are not a guarantee; evaluate the gateway against your own threat model before relying on it.

## Architecture

```text
Browser UI -> FastAPI gateway -> prompt analysis -> allowed or blocked result
                    |
                    +-> optional generation service -> Ollama
```

The gateway API runs at `http://localhost:8000`; its interactive API documentation is at `http://localhost:8000/docs`. The frontend runs at `http://localhost:5173`. Optional generation uses `http://localhost:8001/generate`.

## Quick Start

### Prerequisites

- Python 3.12 or newer
- Node.js 22 or newer and npm
- Windows PowerShell for the one-command launcher

From the repository root, start the API and frontend with:

```powershell
.\run.ps1
```

On first use, the launcher creates `.venv`, installs backend requirements, and runs `npm ci`. It starts both services and writes their output under `logs/`. Press `Ctrl+C` or close the launcher terminal to stop them.

## Local Development

The launcher is intended for Windows PowerShell. To start the API manually from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r api-gateway/requirements.txt
$env:PYTHONPATH = "api-gateway"
python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```powershell
Set-Location frontend
npm ci
npm run dev
```

### Optional Redis History

Analysis history uses Redis and is not required for prompt analysis. Start Redis with Docker Desktop:

```powershell
docker run -d --name securellm-redis -p 6379:6379 redis:7-alpine
$env:REDIS_URL = "redis://localhost:6379/0"
```

History is limited to 50 records per browser session and expires after seven days. If Redis is unavailable, analysis continues but history is unavailable.

### Optional Local LLM

The generation service runs in Docker and connects to Ollama on the host. Start a model in Ollama, then build and run the service from the repository root:

```powershell
ollama run qwen2.5:1.5b
docker build -t securellm-llm ./llm-service
docker run --rm -p 8001:8001 --add-host=host.docker.internal:host-gateway securellm-llm
```

Docker and Ollama are only needed for generation, not for the frontend, gateway, or security analysis. The container accepts `OLLAMA_URL` and `OLLAMA_MODEL` environment variables to override its endpoint and model.

## Run Checks

From the repository root:

```powershell
$env:PYTHONPATH = "api-gateway"
python -m pytest -q tests
```

From `frontend/`:

```powershell
npm ci
npm run lint
npm run build
```

GitHub Actions runs these checks, validates Python syntax and the local launcher contract, and requires pull requests to update a Markdown file under `specs/`.

## Contributing

Bug reports, focused improvements, tests, and documentation are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. The CI-enforced SDD requirement applies to documentation-only changes too.

## Security

Do not post vulnerability details in public issues or discussions. See [SECURITY.md](SECURITY.md) for private reporting guidance.

## License

SecureLLM is licensed under the [Apache License 2.0](LICENSE).
