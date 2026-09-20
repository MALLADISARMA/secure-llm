# SecureLLM Local Development Software Design Document

## Purpose

Local development provides one Windows PowerShell entry point for the API Gateway and React/Vite frontend. The launcher reduces repeated terminal setup while keeping service output available for troubleshooting.

## One-Command Launcher

The repository-root `run.ps1` script:

1. Resolves the repository, API, frontend, and log directories.
2. Creates `.venv` with `python.exe` when the project virtual environment does not exist.
3. Installs API requirements when the SHA-256 fingerprint of `api-gateway/requirements.txt` changes.
4. Runs `npm ci` when frontend dependencies are missing or the SHA-256 fingerprint of `frontend/package-lock.json` changes.
5. Starts Uvicorn for `api-gateway/app/main.py` on port `8000`.
6. Starts the Vite development server from `frontend/` on port `5173`.
7. Starts both services as session-bound PowerShell jobs and redirects standard output and error to `logs/`.

The `logs/` directory is ignored by Git because it contains machine-local runtime output.

## Runtime Requirements

The launcher requires Python with the API dependencies installed and Node.js/npm with frontend dependencies installed. It does not start Docker, Ollama, or the LLM service.

The optional LLM service runs on port `8001` in Docker and calls Ollama on the host at `host.docker.internal:11434`. Its Ollama endpoint and model can be overridden with `OLLAMA_URL` and `OLLAMA_MODEL`. It allows requests from the local frontend origins so the browser can call `/generate`. Security analysis and frontend startup do not depend on the LLM container.

## Verification

The launcher contract is covered by `tests/test_run_script.py`, which verifies hidden process startup, log redirection, expected service directories, and the Uvicorn/Vite commands. GitHub Actions also checks that the launcher and LLM service files exist and validates the launcher contract with shell assertions.

## Failure Handling

The launcher reports startup URLs immediately and remains active while the API and frontend jobs run. Pressing `Ctrl+C` or closing the launcher terminal stops those jobs. Service failures are recorded in `logs/api.error.log` or `logs/frontend.error.log`. A developer should inspect those files when a service is not reachable. If analysis succeeds but generation fails, verify that the LLM container is listening on `8001`, Ollama is running, and the configured model is installed.

## Local Redis History

Redis is an optional backend dependency for analysis history. Kubernetes is not required.

Start Redis with Docker Desktop running:

```powershell
docker run -d --name securellm-redis -p 6379:6379 redis:7-alpine
$env:REDIS_URL = "redis://localhost:6379/0"
```

The gateway uses `GET /history` and `DELETE /history` with the `X-Session-ID` header. History is limited to 50 records per browser session and expires after seven days. If Redis is stopped, `/chat` continues security analysis while history becomes unavailable.