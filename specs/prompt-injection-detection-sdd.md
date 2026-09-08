# Prompt Injection Detection Software Design Document

## Purpose

The SecureLLM API Gateway uses semantic classification to detect prompt injection before an incoming chat request can be forwarded to an LLM service.

## Scope

The detector is implemented in `api-gateway/app/security/prompt_injection.py` as the `detect_prompt_injection` function. It uses the shared classifier in `aiclassifier.py` and is tested independently from the HTTP layer.

## Detection Design

The detector accepts a string message and returns a Boolean result:

- `True` when the prompt-injection confidence is at least `0.70`.
- `False` when the confidence is below `0.70`.

The zero-shot model evaluates semantic meaning, so paraphrased and previously unseen wording can be classified without adding a new phrase to a list.

## API Request Flow

1. FastAPI validates the `POST /chat` request through the `ChatRequest` model.
2. The gateway passes `request.message` to the central analyzer.
3. The analyzer evaluates prompt injection along with the other five security categories.
4. Any category above the threshold receives a blocked response and is not forwarded to an LLM.
5. A message below all thresholds receives the existing allowed response.

Blocked requests return:

```json
{
  "status": "blocked",
  "reason": "Potentially unsafe content detected",
  "message": "Request blocked by SecureLLM Security Gateway"
}
```

Allowed requests continue to return the submitted message with an `allowed` status.

## Testing

`tests/test_promptinjection.py` verifies:

- A normal Kubernetes question is allowed.
- An instruction-override request is detected semantically.
- A paraphrased instruction-override request is detected through mocked model scores.

Run the focused tests from the repository root:

```powershell
python -m pytest tests/test_promptinjection.py
```

## Limitations and Future Work

- Model classification can produce false positives and false negatives.
- The BART model requires additional memory and may need to be downloaded before first use.
- Future work should add labeled evaluation data, model health checks, structured security logging, and configurable thresholds.