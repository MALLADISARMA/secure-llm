# Development

## Repository layout

```text
api-gateway/       FastAPI gateway, classifier, history, and Trivy integration
frontend/          React/Vite application
llm-service/       Optional FastAPI-to-Ollama service and Dockerfile
tests/             Python test suite
specs/             Software design documents required by project CI
docs/              MkDocs documentation source
.github/workflows/ GitHub Actions checks, scans, and Pages publication
run.ps1            Windows launcher for the gateway and frontend
```

## Run checks

From the repository root, install the Python dependencies and run the
backend tests:

```powershell
python -m pip install -r api-gateway/requirements.txt -r llm-service/requirements.txt
$env:PYTHONPATH = "api-gateway"
python -m pytest -q tests
```

Check the frontend from `frontend/`:

```powershell
npm ci
npm run lint
npm run build
```

GitHub Actions also checks Python syntax and the local launcher contract.
Pull requests to `main` must update a Markdown document under `specs/`; see
[CONTRIBUTING.md](https://github.com/MALLADISARMA/secure-llm/blob/main/CONTRIBUTING.md).

## Documentation site

Install the documentation requirements from the repository root and launch a
live-reloading preview:

```powershell
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

Open the address printed by MkDocs (normally `http://127.0.0.1:8000`). Build
the site using the same strict mode as CI:

```powershell
python -m mkdocs build --strict
```

The generated site is written to `site/`, which is a build artifact and should
not be edited directly.

## GitHub Pages

`.github/workflows/docs.yml` builds documentation on pull requests to `main`,
and builds and deploys it on pushes to `main` or a manual workflow dispatch.
To enable publication, open the repository's **Settings → Pages** and select
**GitHub Actions** as the build and deployment source. The workflow uses the
official Pages artifact and deployment actions; it does not need a deployment
token secret.

## Contribution notes

Keep the README useful as a quick-start overview, and place detailed product
guidance in `docs/`. Update the relevant SDD under `specs/` when changing
project behavior, because the existing CI requires an SDD update on pull
requests.
