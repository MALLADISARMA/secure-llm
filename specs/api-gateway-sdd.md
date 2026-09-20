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

The request body is validated by the `ChatRequest` Pydantic model. Missing, blank, non-string, or overlong `message` values are rejected with HTTP `422`. Messages are limited to 10,000 characters.

Allowed response:

The `analysis.results` array contains one object for each of the six security categories. The example below abbreviates that array for readability.

```json
{
  "status": "allowed",
  "message": "Explain Kubernetes networking",
  "analysis": {
    "allowed": true,
    "blocked": false,
    "overall_score": 5.0,
    "highest_risk": "Prompt Injection",
    "results": "six category result objects"
  }
}
```

Blocked response:

The blocked response uses the same complete `analysis` shape as an allowed response.

```json
{
  "status": "blocked",
  "reason": "Potentially unsafe content detected",
  "message": "Request blocked by SecureLLM Security Gateway",
  "analysis": {
    "allowed": false,
    "blocked": true,
    "overall_score": 95.0,
    "highest_risk": "Prompt Injection",
    "results": "six category result objects"
  }
}
```

## Request Flow

1. FastAPI parses and validates the JSON body.
2. The gateway sends the message to the central semantic analyzer.
3. The analyzer scores six security categories using the zero-shot classification model.
4. A category is detected when its confidence is at least `0.70`.
5. Any detected category blocks the request and prevents LLM forwarding.
6. The response includes both the gateway status and the complete analyzer result so the frontend can render risk and category details. LLM forwarding will be added in a later change.

## Semantic Security Analysis

`app/security/aiclassifier.py` loads and caches `facebook/bart-large-mnli` through Hugging Face Transformers. The analyzer in `app/security/analyzer.py` evaluates:

- Prompt Injection
- Jailbreak
- PII / Sensitive Data
- System Prompt Leakage
- Toxicity
- Malicious Intent

The analyzer returns an overall score, highest-risk category, and per-category confidence, detection, and severity values. The API exposes this result under `analysis` in both allowed and blocked responses.

## Local Verification

From `api-gateway/`, install dependencies and start the development server:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

From the repository root, run the backend checks with:

```powershell
python -m pytest -q
```

From `frontend/`, run the frontend checks with:

```powershell
npm ci
npm run lint
npm run build
```

Use `http://127.0.0.1:8000/docs` to execute both endpoints interactively. The root health endpoint can also be opened directly in a browser.

## Analysis History

The gateway stores completed security analyses in Redis using session-scoped keys:

```text
securellm:history:{session_id}
```

The frontend stores a random session ID in `localStorage` and sends it as `X-Session-ID`. The gateway validates this value before constructing a Redis key. Each session is limited to 50 records and history keys expire after seven days. Records include the prompt, status, score, highest-risk category, complete analysis, record ID, session ID, and a UTC timestamp. LLM responses are not stored.

### History endpoints

- `GET /history` returns the current session's records, newest first.
- `DELETE /history` deletes only the current session's records.

Both endpoints require `X-Session-ID`. Redis is optional for `/chat`: connection failures do not change security analysis or block the normal response. History endpoints report unavailable storage when Redis cannot be reached.

The Redis URL is configured with `REDIS_URL`, defaulting to `redis://localhost:6379/0`. Redis is never exposed to the frontend. Prompts may contain PII or secrets, so production deployments require authentication, TLS, restricted network access, authorization, and retention controls.

## Future Changes

- Add model loading configuration and health checks for production deployments.
- Add model-based moderation evaluation and calibration against labeled security prompts.
- Forward allowed requests to the configured vLLM or LLM service.
- Add structured logging, authentication, rate limiting, and output security checks.
