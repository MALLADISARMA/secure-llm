# Prompt Injection Detection Software Design Document

## Purpose

This change adds an initial security check to the SecureLLM API Gateway. The gateway detects common prompt-injection and jailbreak phrases before an incoming chat request can be forwarded to an LLM service.

## Scope

The detector is implemented in `api-gateway/security/promptinjection.py` as the `detect_prompt_injection` function. The security logic was moved out of `api-gateway/app/main.py` so it can be tested and extended independently from the HTTP layer.

## Detection Design

The detector accepts a string message and returns a Boolean result:

- `True` when the message contains a configured suspicious phrase.
- `False` when no configured phrase is found.

Detection is case-insensitive. The initial rule set covers:

- Attempts to ignore previous or current instructions.
- Requests to reveal the system or prompt.
- The term `jailbreak`.

Matching uses substring checks. This is intentionally a small, deterministic first implementation rather than a complete prompt-security model.

## API Request Flow

1. FastAPI validates the `POST /chat` request through the `ChatRequest` model.
2. The gateway passes `request.message` to `detect_prompt_injection`.
3. A matching message receives a blocked response and is not forwarded to an LLM.
4. A non-matching message receives the existing allowed response.

Blocked requests return:

```json
{
  "status": "blocked",
  "reason": "Potential prompt injection detected",
  "message": "Request blocked by SecureLLM Security Gateway"
}
```

Allowed requests continue to return the submitted message with an `allowed` status.

## Testing

`tests/test_promptinjection.py` verifies:

- A normal Kubernetes question is allowed.
- An instruction-override request is detected.
- A jailbreak request is detected.

Run the focused tests from the repository root:

```powershell
python -m pytest tests/test_promptinjection.py
```

## Limitations and Future Work

- Phrase matching can miss novel or obfuscated attacks and may produce false positives.
- The suspicious-pattern list is currently hard-coded.
- API-level tests should be added for blocked, allowed, and invalid `/chat` requests.
- Future work can introduce configurable policies, structured security logging, and additional detection methods before forwarding allowed requests to an LLM service.