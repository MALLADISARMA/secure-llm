# Security and limitations

SecureLLM is an evolving local project and should not be treated as a
production security boundary. Model-based detection can produce false
positives and false negatives. A threshold decision does not establish that a
prompt is safe.

## Important boundaries

- The browser submits analysis to the gateway, then submits an allowed prompt
  directly to the separate LLM service. The gateway is not a network proxy
  that can enforce policy for arbitrary clients.
- The current services do not implement user authentication or authorization.
- `POST /security/scan` accepts a filesystem path and runs the local Trivy
  executable. Keep the gateway private to a trusted local environment; do not
  expose this endpoint to untrusted callers.
- The scanner is configured for vulnerability findings, not a complete
  malware or source-code security review.
- The gateway permits the local Vite origins at ports `5173` and
  `127.0.0.1:5173`; this CORS setup is development-oriented.
- The History page stores submitted prompts and analysis in Redis when it is
  available. Those values are not encrypted by this application before
  storage. Treat Redis and its network as sensitive.
- Session IDs scope history but are not authentication credentials. Anyone
  who can obtain an ID may be able to request that session's history if they
  can reach the gateway.
- The generation endpoint does not independently enforce the gateway's
  decision. Restrict service access and do not rely on the browser as an
  authorization layer.

## Data and model behavior

Prompts are sent to the local gateway for classification. If the UI permits
the prompt, it is sent to the local LLM service and onward to Ollama. Model
weights for the classifier may need to be downloaded from Hugging Face when
first loaded, depending on the local cache and network configuration.

When Redis is enabled, prompt text and analysis are retained for up to 50
records per browser session with a seven-day expiry. Clearing history deletes
the current session's Redis key. Running without Redis permits analysis, but
not history.

## Deployment guidance

The repository documents local development, not a hardened production
deployment. Before adapting it for a real application, evaluate at least:

- authentication, authorization, and network isolation for every service;
- request limits, resource usage, and model availability under load;
- privacy, retention, access controls, and transport protection for prompts;
- detector quality using representative adversarial and benign inputs;
- policy handling for model failures, scanner errors, and unavailable
  dependencies;
- a threat model for the application that consumes the analysis result.

For vulnerability reporting, follow
[`SECURITY.md`](https://github.com/MALLADISARMA/secure-llm/blob/main/SECURITY.md).
Do not publish sensitive vulnerability details in a public issue.
