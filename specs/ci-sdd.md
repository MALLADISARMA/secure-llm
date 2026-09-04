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
3. Install Python dependencies from `requirements.txt` when that file exists.
4. Run the test suite when a `tests/` directory exists.
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

## Failure Behavior

- Missing root dependencies: dependency installation is skipped.
- Missing tests directory: test execution is skipped.
- Missing SDD update on a pull request: the workflow fails.
- Any command failure in the active workflow step causes CI to fail.

## Change Contract

Any feature, bug fix, API change, or CI change should include a relevant Markdown update in `specs/`. The SDD should describe the changed behavior, validation approach, and any future work that remains.

## Future Improvements

- Add a root `requirements.txt` or update the workflow to install dependencies from `api-gateway/requirements.txt`.
- Add automated API tests for `GET /` and `POST /chat`.
- Add linting, formatting, and type-checking stages.
- Upload test and coverage reports as CI artifacts.
