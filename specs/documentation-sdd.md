# MkDocs project documentation SDD

## Purpose

Provide a navigable project guide that explains the implemented SecureLLM
features, architecture, API, security behavior, setup, and technology choices.
Publish the guide as a GitHub Pages site from the `main` branch.

## Design

- MkDocs Material uses Markdown sources in `docs/` and the root `mkdocs.yml`
  navigation.
- `requirements-docs.txt` declares the documentation build dependency.
- `.github/workflows/docs.yml` builds with `mkdocs build --strict` on pull
  requests and deploys the Pages artifact on pushes to `main` and manual
  dispatches.
- The workflow uses GitHub's Pages artifact/deployment actions and scoped
  permissions; no repository deployment secret is required.
- The README links to the documentation source and explains the Pages
  prerequisite.
- The README's security-check overview distinguishes the zero-shot prompt
  classifier (`facebook/bart-large-mnli`) from the optional Ollama response
  model (`qwen2.5:1.5b`), summarizes the six analyzed categories and the
  `0.70` blocking threshold, and notes the supplemental text-pattern checks
  and separate Trivy vulnerability scanner.

## Verification

Run `python -m mkdocs build --strict` from the project root. Configure the
repository's Pages source as **GitHub Actions** to enable deployment.

## Scope

Documentation describes the current implementation; it does not add product
features or claim the prompt classifier is a complete security control.
