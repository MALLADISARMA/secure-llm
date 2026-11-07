# SecureLLM documentation

SecureLLM is a local-first prompt-security demonstration. Its FastAPI gateway
classifies a prompt before the browser sends an allowed prompt to a separate
local language-model service. It also provides an optional, session-scoped
history and a separate API endpoint for local Trivy filesystem scans.

This documentation describes the implementation in this repository. It is not
a claim that the detector is complete or suitable as the only protection for a
production LLM system.

## Project overview

SecureLLM is a local-first demonstration of a prompt-security gateway. The
React/Vite browser submits prompts to a FastAPI gateway, which scores them
against six security categories before the browser decides whether to send an
allowed prompt to a separate, optional Ollama-backed generation service.
Optional Redis stores session-scoped analysis history. The gateway also has a
separate API for local Trivy filesystem vulnerability scans.

The gateway's security model is **`facebook/bart-large-mnli`**, used through
Hugging Face Transformers for zero-shot classification. It scores category
labels without a SecureLLM-specific training step; a score of 0.70 or higher
in any category blocks the prompt in the application flow. This is a
classification model, not the chat-generation model. See
[Security analysis](security-analysis.md) for what each category means, how
scoring works, and the model's limitations. The optional response model is
`qwen2.5:1.5b`, served locally by Ollama.

## Find your way around

- [Getting started](getting-started.md) — prerequisites and local run modes.
- [Features](features.md) — how the dashboard, analyzer, history, and scans
  work.
- [Security analysis](security-analysis.md) — categories, scoring, and
  allow/block behavior.
- [Architecture](architecture.md) — services, data flow, and boundaries.
- [API reference](api-reference.md) — gateway and generation endpoints.
- [Technology choices](technology-stack.md) — technologies in use and their
  roles in this project.
- [Security and limitations](security-and-limitations.md) — data handling,
  deployment cautions, and known limits.
- [Development](development.md) — checks, contribution pointers, and the docs
  site workflow.

## At a glance

| Component | Responsibility | Local address |
| --- | --- | --- |
| React/Vite frontend | Dashboard, prompt analyzer, and history UI | `http://localhost:5173` |
| FastAPI API gateway | Prompt classification, policy decision, history API, and scan API | `http://localhost:8000` |
| Redis (optional) | Session-scoped history storage | `localhost:6379` |
| FastAPI LLM service (optional) | Forwards an allowed prompt to Ollama | `http://localhost:8001` |
| Ollama (optional) | Runs the configured local model | `localhost:11434` |

## Project status

Implemented features are described in [Features](features.md). RAG document
scanning, tool authorization, Kubernetes deployment, authentication, and
production-grade policy management are not implemented.

The [README](https://github.com/MALLADISARMA/secure-llm/blob/main/README.md)
remains the fastest path to start the app. For security concerns, follow the
private reporting guidance in
[`SECURITY.md`](https://github.com/MALLADISARMA/secure-llm/blob/main/SECURITY.md).
