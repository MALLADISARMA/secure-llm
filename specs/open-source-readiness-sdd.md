# Open-Source Repository Readiness Software Design Document

## Purpose

The repository provides the public-facing documentation and licensing needed for external users and contributors to understand, run, test, and report issues in SecureLLM.

## Repository Contract

The repository root contains:

- `README.md` with current capabilities, limitations, setup, optional services, and validation commands.
- `LICENSE` with the Apache License 2.0 terms.
- `CONTRIBUTING.md` with contributor setup, checks, pull-request expectations, and the SDD requirement.
- `SECURITY.md` with private vulnerability-reporting guidance.
- `specs/` with design documentation required by the pull-request CI check.

The GitHub Actions repository check validates the required files before installing dependencies. `tests/test_repository_contract.py` verifies the same public metadata and README references locally.

## Validation

The documented checks match the CI workflow:

```powershell
$env:PYTHONPATH = "api-gateway"
python -m pytest -q tests

Set-Location frontend
npm ci
npm run lint
npm run build
```

The CI workflow also compiles Python sources, validates the PowerShell launcher contract, and requires a changed Markdown file under `specs/` for pull requests.

## Limitations

The security classifier is a probabilistic control and is not a complete security boundary. Users must review the threat model, protect access to the gateway, avoid committing secrets, and evaluate model behavior against representative data before production use.
