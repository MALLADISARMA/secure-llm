# API Gateway Software Design Document

## Scope

This change establishes the first testable HTTP contract for the SecureLLM API Gateway. The service is implemented with FastAPI and currently runs as a local application before integration with an LLM service.

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
  "reason": "Potential prompt injection detected",
  "message": "Request blocked by SecureLLM Security Gateway"
}
```

## Request Flow

1. FastAPI parses and validates the JSON body.
2. The gateway lowercases the message and checks it against the initial rule-based prompt-injection patterns.
3. Matching messages are blocked and are not forwarded to an LLM.
4. Non-matching messages are returned as allowed responses. LLM forwarding will be added in a later change.

## Local Verification

From `api-gateway/`, install dependencies and start the development server:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Use `http://127.0.0.1:8000/docs` to execute both endpoints interactively. The root health endpoint can also be opened directly in a browser.

## Future Changes

- Replace the initial pattern list with a configurable security policy.
- Add automated API tests for allowed, blocked, and invalid requests.
- Forward allowed requests to the configured vLLM or LLM service.
- Add structured logging, authentication, rate limiting, and output security checks.
