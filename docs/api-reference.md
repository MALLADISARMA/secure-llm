# API reference

The gateway's interactive OpenAPI reference is available at
[`http://localhost:8000/docs`](http://localhost:8000/docs) while the gateway
is running. Its schema is also available at `/openapi.json`.

## Gateway

Base URL: `http://localhost:8000`

### `GET /`

Returns gateway name, status, and version.

### `POST /chat`

Analyze a prompt. Requires an `X-Session-ID` header containing 1–128
letters, digits, underscores, or hyphens. The request body is:

```json
{
  "message": "A prompt to analyze"
}
```

`message` must be non-empty, at most 10,000 characters, and not whitespace
only. The gateway returns an analysis with `allowed`, `blocked`,
`overall_score`, `highest_risk`, and six category result objects.

An allowed response has `status: "allowed"` and includes the submitted message
and analysis. A blocked response has `status: "blocked"`, a generic reason,
and analysis. Both outcomes are written to history when Redis is available.
The response does not contain an LLM-generated answer.

Example analysis shape:

```json
{
  "allowed": true,
  "blocked": false,
  "overall_score": 18.5,
  "highest_risk": "Toxicity",
  "results": [
    {
      "category": "Prompt Injection",
      "detected": false,
      "confidence": 0.0123,
      "severity": "NONE"
    }
  ]
}
```

The actual `results` array contains all six security categories.

### `GET /history`

Requires `X-Session-ID`. Returns the current session's records and count.
When Redis is unavailable, returns `status: "unavailable"` with an empty
records array and a message. Successful records are ordered newest first.

### `DELETE /history`

Requires `X-Session-ID`. Deletes only the current session's history. Returns
`status: "unavailable"` if Redis cannot be reached.

### `POST /security/scan`

Runs the local Trivy binary against a filesystem path. Body:

```json
{
  "path": "C:\\path\\to\\scan"
}
```

Returns `summary` counts for `critical`, `high`, `medium`, `low`, and
`unknown`, plus a list of vulnerability records. Returns HTTP 500 if the
scanner reports a runtime failure. Trivy must be installed and available on
the gateway process's `PATH`.

This endpoint has no authentication or authorization in the current
implementation. Do not expose it to untrusted clients; see
[Security and limitations](security-and-limitations.md).

## Local LLM service

Base URL: `http://localhost:8001`

### `GET /health`

Returns `{"status":"UP"}` when the FastAPI process is responding. This does not
guarantee that Ollama or the configured model can generate successfully.

### `POST /generate`

Accepts a JSON body containing a `message` string, sends it to Ollama using
the configured model, and returns:

```json
{
  "response": "Generated text"
}
```

Generation failures are returned as HTTP 500. The request model does not set
the same explicit length bounds as the gateway's chat model.

## Browser session header

The frontend creates a session ID with `crypto.randomUUID()` when available,
stores it under `securellm_session_id` in `localStorage`, and sends it as
`X-Session-ID`. This header scopes history; it is not user authentication.
