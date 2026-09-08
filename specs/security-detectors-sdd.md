# Security Detector Software Design Document

## Purpose

This change documents and tests the semantic security detectors under `api-gateway/app/security`. The detectors use shared zero-shot classification scores rather than fixed phrase lists, allowing paraphrased and previously unseen wording to be evaluated.

## Scope

The covered detectors are:

- `detect_jailbreak` in `jailbreak.py`
- `detect_malicious_intent` in `maliciousintent.py`
- `detect_pii` in `pii.py`
- `detect_prompt_leakage` in `promptleakage.py`
- `detect_toxicity` in `toxicity.py`

Prompt-injection behavior remains covered by `prompt-injection-detection-sdd.md` and `detect_prompt_injection`.

## Detector Contracts

Each detector accepts a string and returns `True` when its model score is at least `0.70`; otherwise it returns `False`. The shared model is loaded once through an LRU cache.

### Jailbreak

Detects attempts to bypass safety controls, including requests to ignore safety rules, enable unrestricted or developer modes, or remove restrictions.

### Malicious intent

Detects explicit harmful actions such as bypassing authentication, stealing credentials, creating malware or ransomware, phishing, and data exfiltration.

### PII

Detects PII or requests involving sensitive information through the semantic label `PII or sensitive information`.

### Prompt leakage

Detects requests to reveal system prompts, hidden instructions, or the instructions provided to the assistant.

### Toxicity

Detects abusive, hateful, or threatening content.

## API Integration

The `POST /chat` endpoint invokes `is_unsafe_message`, which delegates to `analyze_prompt`. The request is blocked when any of the six category scores reaches the threshold. The blocked response uses the generic reason `Potentially unsafe content detected` because the current API does not expose detector-specific reasons.

## Testing

Tests are located in `tests/test_security_detectors.py`, `tests/test_analyzer.py`, `tests/test_api_gateway.py`, and `tests/test_promptinjection.py`. The shared fixture in `tests/conftest.py` mocks model scores, so tests are deterministic and do not download or run the BART model.

Run from the repository root after installing the API and test dependencies:

```powershell
python -m pip install -r api-gateway/requirements.txt pytest httpx
python -m pytest tests
```

## Limitations

- Model classification can produce false positives and false negatives and must be evaluated against representative labeled data.
- The default model is large and may require substantial memory and startup time.
- Model downloads require network access unless the model is pre-cached.
- The current API does not expose analyzer details or detector-specific reasons.