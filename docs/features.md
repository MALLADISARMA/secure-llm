# Features

## Dashboard

The dashboard links to the Analyzer and summarizes the six security
categories and the semantic classification engine. It is an informational
frontend view; its displayed gateway status is not a live health check.

## Prompt analyzer

The Analyzer accepts a prompt and follows this sequence:

1. The browser sends the text to `POST /chat` on the gateway with its
   `X-Session-ID`.
2. The gateway evaluates the prompt and returns the category results and an
   `allowed` or `blocked` status.
3. The analysis is saved to Redis when Redis is available.
4. Only for an `allowed` result, the browser separately sends the prompt to
   `POST /generate` on the LLM service.
5. The page displays the security results and, when generation succeeds, the
   model response.

A blocked prompt is not sent to the LLM service by this UI flow. The gateway
does not itself generate a model response or proxy the generation request.

## Analysis history

The browser creates a session identifier and retains it in `localStorage`.
History requests send that identifier in `X-Session-ID`; the gateway validates
it and uses it to scope the Redis key. The History page can display and clear
the current session's records.

The history service retains no more than 50 newest records per session. Its
seven-day TTL is refreshed when a new record is saved. If Redis is unavailable,
the gateway can continue analyzing prompts, but history requests report that
storage is unavailable.

## Filesystem vulnerability scans

The gateway exposes `POST /security/scan`, which runs the local Trivy
executable against a caller-supplied filesystem path and returns a severity
summary and vulnerability details. This API is not connected to a frontend
page and is not the same process as the GitHub Actions scan.

Separately, `.github/workflows/trivy-scan.yml` runs a Trivy vulnerability
filesystem scan against the checked-out repository every Monday or on manual
dispatch. It uploads SARIF findings to GitHub Code Security when available.
The workflow reports vulnerabilities but does not fail solely because
findings exist.

## Not implemented

This repository does not currently implement RAG or document scanning,
authorization of model tools, Kubernetes deployment, accounts, user
authentication, or production policy administration. See
[Security and limitations](security-and-limitations.md) before using the
project outside a local demonstration.
