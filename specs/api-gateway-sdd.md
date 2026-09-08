# API Gateway Software Design Document

## Scope

The SecureLLM API Gateway is implemented with FastAPI and uses semantic security analysis before a request can be forwarded to an LLM service.

## API Contract

### `GET /`

Returns a health response showing that the gateway is running.

Example response:

```json
{
  "service": "SecureLLM API Gateway",
  "status": "running",
  "version": "0.1.0"
}
```

### `POST /chat`

Accepts a JSON request body with one required string field:

```json
{
  "message": "Explain Kubernetes networking"
}
```

The request body is validated by the `ChatRequest` Pydantic model. Missing or invalid `message` values are rejected by FastAPI with HTTP `422`.

Allowed response:

```json
{
  "status": "allowed",
  "message": "Explain Kubernetes networking"
}
```

Blocked response:

```json
{
  "status": "blocked",
  "reason": "Potentially unsafe content detected",
  "message": "Request blocked by SecureLLM Security Gateway"
}
```

## Request Flow

1. FastAPI parses and validates the JSON body.
2. The gateway sends the message to the central semantic analyzer.
3. The analyzer scores six security categories using the zero-shot classification model.
4. A category is detected when its confidence is at least `0.70`.
5. Any detected category blocks the request and prevents LLM forwarding.
6. Messages with no detected category are returned as allowed responses. LLM forwarding will be added in a later change.

## Semantic Security Analysis

`app/security/aiclassifier.py` loads and caches `facebook/bart-large-mnli` through Hugging Face Transformers. The analyzer in `app/security/analyzer.py` evaluates:

- Prompt Injection
- Jailbreak
- PII / Sensitive Data
- System Prompt Leakage
- Toxicity
- Malicious Intent

The analyzer returns an overall score, highest-risk category, and per-category confidence, detection, and severity values. The API currently exposes only the allowed or blocked response.

## Local Verification

From `api-gateway/`, install dependencies and start the development server:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Use `http://127.0.0.1:8000/docs` to execute both endpoints interactively. The root health endpoint can also be opened directly in a browser.

## Future Changes

- Add model loading configuration and health checks for production deployments.
- Add model-based moderation evaluation and calibration against labeled security prompts.
- Forward allowed requests to the configured vLLM or LLM service.
- Add structured logging, authentication, rate limiting, and output security checks.
