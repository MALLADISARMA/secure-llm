# SecureLLM CI Software Design Document

## Purpose

The SecureLLM CI workflow validates repository changes on every push and pull request. It provides a lightweight build check and enforces that project changes include the required SDD documentation.

## Workflow

The workflow is defined in `.github/workflows/build.yml` and runs on:

- Every branch push
- Pull requests targeting `main`

The workflow uses Ubuntu and Python 3.12.

## Pipeline Stages

1. Check out the repository with full history.
2. Confirm that the repository checkout succeeded.
3. Install Python dependencies from `api-gateway/requirements.txt`.
4. Run the complete test suite from the repository root with `PYTHONPATH=api-gateway`.
5. On pull requests, compare the branch with `origin/main` and require at least one changed Markdown file under `specs/`.
6. Report successful completion.

## SDD Enforcement

The pull-request check runs:

```text
git diff --name-only origin/main...HEAD
```

The check passes when the changed-file list contains a path matching:

```text
specs/*.md
```

A pull request without an SDD update fails with an instruction to update the `specs/` directory and commit the change.

## Contributor Requirement

The contribution guide requires an SDD update for every project change, including:

- Features and bug fixes
- API, backend, and frontend changes
- CI/CD and infrastructure changes
- Security, testing, and documentation changes

Contributors must add or update a Markdown file under `specs/` describing what changed, why it changed, how it was tested, and any relevant future work. The pull-request checklist includes this requirement so it is reviewed before merge.

## Failure Behavior

- Missing `api-gateway/requirements.txt`: dependency installation fails.
- Missing `tests/` directory: test execution fails.
- Missing SDD update on a pull request: the workflow fails.
- Any command failure in the active workflow step causes CI to fail.

## Change Contract

Any feature, bug fix, API change, CI change, security change, testing change, or documentation change should include a relevant Markdown update in `specs/`. The SDD should describe the changed behavior, rationale, validation approach, and any future work that remains.

## Future Improvements

- Add linting, formatting, and type-checking stages.
- Upload test and coverage reports as CI artifacts.
