# Getting started

The supported launcher is designed for Windows PowerShell. You can start the
gateway and browser UI without Redis, Docker, or Ollama; those optional
services enable history and generated responses.

## Prerequisites

- Windows 10/11 with PowerShell.
- Python 3.12 or newer.
- Node.js 22 or newer and npm.
- Docker Desktop with Linux containers, when using the Redis or LLM containers.
- Ollama and the configured model, when generating LLM responses.

The gateway loads `facebook/bart-large-mnli` through Hugging Face Transformers
when the first prompt is classified. The model must be available locally or
downloadable in the environment where the gateway runs.

## Start the gateway and frontend

From the repository root (`secure-llm/`), run:

```powershell
.\run.ps1
```

On first use, the launcher creates `.venv`, installs
`api-gateway/requirements.txt`, and installs the frontend packages with
`npm ci`. It starts the gateway at `http://localhost:8000` and Vite at
`http://localhost:5173`. Use `Ctrl+C` or close that terminal to stop the
services.

This launcher does **not** start Redis, Docker, Ollama, or the LLM service.
Prompt analysis can still run without Redis; history and generated responses
will not be available until their corresponding services are started.

## Enable history with Redis

With Docker Desktop running, start Redis from the repository root:

```powershell
docker run -d --name securellm-redis --restart unless-stopped `
    -p 6379:6379 redis:7-alpine
```

Set the gateway's Redis connection string before starting `run.ps1`:

```powershell
$env:REDIS_URL = "redis://localhost:6379/0"
.\run.ps1
```

The default is already `redis://localhost:6379/0`. History is stored for at
most 50 records per browser session and expires seven days after its latest
write.

## Enable local LLM responses

Install and start Ollama, then download the default model:

```powershell
ollama pull qwen2.5:1.5b
```

Build the LLM service image from the repository root:

```powershell
docker build -t securellm-llm:local ./llm-service
```

Start the service container. The address `host.docker.internal` lets the
container call Ollama on the Windows host:

```powershell
docker run -d --name securellm-llm --restart unless-stopped `
    -p 8001:8001 `
    --add-host=host.docker.internal:host-gateway `
    -e OLLAMA_URL=http://host.docker.internal:11434/api/generate `
    -e OLLAMA_MODEL=qwen2.5:1.5b `
    securellm-llm:local
```

Check that the service is up:

```powershell
Invoke-RestMethod http://localhost:8001/health
```

After starting the API and frontend, visit `http://localhost:5173`. The
Analyzer sends the prompt to the gateway first and calls the LLM service only
if the gateway returns `allowed`.

## Run services manually

Start the gateway in one PowerShell window:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r api-gateway/requirements.txt
$env:PYTHONPATH = "api-gateway"
python -m uvicorn app.main:app --reload --port 8000
```

Start the frontend in another:

```powershell
Set-Location frontend
npm ci
npm run dev
```

To stop optional containers:

```powershell
docker stop securellm-llm securellm-redis
```

For complete setup guidance and troubleshooting context, see the root
[README](https://github.com/MALLADISARMA/secure-llm/blob/main/README.md).
