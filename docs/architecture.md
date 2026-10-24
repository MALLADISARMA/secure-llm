# Architecture

## Components

| Component | Implementation | Purpose |
| --- | --- | --- |
| Browser UI | React 19, React Router, Vite | Dashboard, Analyzer, and History pages |
| API gateway | FastAPI, Pydantic | Prompt analysis, session history API, local scan API |
| Classifier | Hugging Face Transformers and PyTorch | Zero-shot classification with BART MNLI |
| History store | Redis (optional) | Bounded, expiring session histories |
| LLM API | Separate FastAPI service | Accepts generation requests and calls Ollama |
| Model runtime | Ollama (optional) | Runs `qwen2.5:1.5b` by default |
| Repository scan | GitHub Actions and Trivy | Scheduled/manual dependency and filesystem vulnerability scan |

## Prompt flow

1. The frontend creates or reuses a random session ID in browser
   `localStorage`.
2. It submits the prompt and ID to the gateway's `/chat` endpoint.
3. The gateway validates the ID, runs `analyze_prompt`, and evaluates the
   threshold policy.
4. It attempts to save the prompt and analysis to the session's Redis list.
   Redis is optional for analysis.
5. The gateway returns `allowed` or `blocked` plus the analysis.
6. If allowed, the frontend makes a separate request to the LLM service. That
   service sends a non-streaming request to Ollama and returns its response.

The browser-to-LLM request is separate from the browser-to-gateway request.
The gateway decision governs the supplied UI flow; it is not an enforcement
proxy for other clients or direct access to the LLM service.

## History flow

The frontend adds `X-Session-ID` to history and chat requests. The gateway
accepts only IDs matching letters, digits, underscores, and hyphens, with a
maximum length of 128 characters. Redis keys use the prefix
`securellm:history:`. The service keeps the newest 50 records and refreshes a
seven-day expiry on writes.

## Scan flows

`POST /security/scan` calls the gateway's local `TrivyScanner`, which invokes
`trivy fs --scanners vuln` for the supplied path. The scheduled GitHub Actions
workflow instead scans the repository checkout in its runner and uploads
SARIF. The browser does not call either scan flow.

## Runtime addresses

- Frontend: `http://localhost:5173`
- Gateway: `http://localhost:8000`; interactive OpenAPI docs at `/docs`
- LLM service: `http://localhost:8001`; health check at `/health`
- Ollama: `http://localhost:11434` by default
- Redis: `localhost:6379` by default

The root
[README](https://github.com/MALLADISARMA/secure-llm/blob/main/README.md)
includes the current Windows launcher and container commands.
