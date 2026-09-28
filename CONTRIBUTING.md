# Contributing

Thanks for helping improve SecureLLM. Focused bug fixes, tests, and documentation improvements are welcome.

## Development Setup

See [README.md](README.md#local-development) for prerequisites and service setup. The one-command launcher is intended for Windows PowerShell; the API and frontend can also be started separately.

## Run the Checks

From the repository root, run the backend test suite:

```powershell
$env:PYTHONPATH = "api-gateway"
python -m pytest -q tests
```

From `frontend/`, install dependencies and run the checks used by CI:

```powershell
npm ci
npm run lint
npm run build
```

GitHub Actions also checks Python syntax and the local launcher contract.

## Design Document Requirement

Every pull request must add or update a Markdown file under `specs/`. The CI workflow enforces this for all pull requests, including documentation-only changes. Describe the change, its rationale, how it was verified, and any relevant follow-up work.

## Pull Requests

1. Fork the repository and create a branch for your change.
2. Keep the pull request focused and include tests for behavior changes.
3. Update relevant documentation and the required SDD under `specs/`.
4. Run the applicable checks above and confirm they pass.
5. Open a pull request that explains the problem, solution, validation, and security impact where applicable.

Before submitting, check that you have not included credentials, personal data, generated files, or unrelated changes.

## License

By intentionally submitting a contribution for inclusion in this project, you agree that it is submitted under the [Apache License 2.0](LICENSE), subject to its terms.