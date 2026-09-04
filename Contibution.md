# Contributing to SecureLLM 🤝

Thank you for your interest in contributing to SecureLLM!

SecureLLM is an open-source project focused on **LLM applications, AI security, RAG, and Kubernetes**.

We welcome contributions in:

* AI security
* Prompt injection detection
* Jailbreak detection
* PII detection
* RAG security
* Backend development
* Frontend development
* Kubernetes
* Helm
* Kubernetes security
* Monitoring
* Testing
* CI/CD
* Documentation

---

# 🔐 Contribution Policy

The `main` branch is protected.

**Contributors must not push directly to `main`.**

All changes must go through:

```text
Contributor
     ↓
Create Branch
     ↓
Make Changes
     ↓
Run Tests
     ↓
Push Branch
     ↓
Open Pull Request
     ↓
CI Checks
     ↓
Maintainer Review
     ↓
Approval
     ↓
Merge into main
```

This keeps the main branch stable and ensures that every contribution is reviewed.

---

# 🚀 Getting Started

## 1. Fork the Repository

Fork the SecureLLM repository to your own GitHub account.

Then clone your fork:

```bash
git clone https://github.com/<your-username>/secure-llm.git
```

Move into the project:

```bash
cd secure-llm
```

---

# 🔗 2. Add the Upstream Repository

Add the original SecureLLM repository as `upstream`:

```bash
git remote add upstream https://github.com/<maintainer-username>/secure-llm.git
```

Check your remotes:

```bash
git remote -v
```

You should see something similar to:

```text
origin    https://github.com/<your-username>/secure-llm.git
upstream  https://github.com/<maintainer-username>/secure-llm.git
```

`origin` = your fork

`upstream` = original SecureLLM repository

---

# 🌿 3. Create a Feature Branch

Never work directly on `main`.

First update your local main branch:

```bash
git checkout main
git pull upstream main
```

Create a new branch:

```bash
git checkout -b feature/prompt-injection-detection
```

---

# 🏷️ Branch Naming

Use descriptive branch names.

### New Feature

```text
feature/<feature-name>
```

Example:

```text
feature/prompt-injection-detection
```

### Bug Fix

```text
fix/<bug-name>
```

Example:

```text
fix/rag-retrieval-error
```

### Documentation

```text
docs/<topic>
```

Example:

```text
docs/kubernetes-security
```

### Testing

```text
test/<topic>
```

Example:

```text
test/prompt-injection-tests
```

### Security

```text
security/<topic>
```

Example:

```text
security/pii-detector
```

### Refactoring

```text
refactor/<topic>
```

Example:

```text
refactor/security-gateway
```

---

# 💻 4. Make Your Changes

Work only on your assigned feature or issue.

For example:

```text
feature/prompt-injection-detection
```

could contain:

* Prompt injection detector
* Unit tests
* Documentation

Avoid unrelated changes in the same Pull Request.

---

# 🧪 5. Run Tests Locally

Before creating a Pull Request, run the relevant tests.

Python:

```bash
pytest
```

Linting:

```bash
ruff check .
```

Frontend:

```bash
npm test
```

Additional tests may be added as the project grows.

---

# 📦 6. Check Your Changes

Run:

```bash
git status
```

Review the files you changed.

You can inspect the differences using:

```bash
git diff
```

Make sure you are not committing:

* API keys
* Passwords
* Tokens
* Kubernetes secrets
* Personal information
* Unnecessary files

---

# 💾 7. Commit Your Changes

Add the files:

```bash
git add .
```

Create a meaningful commit:

```bash
git commit -m "feat: add prompt injection detector"
```

Recommended commit prefixes:

```text
feat:
fix:
docs:
test:
security:
refactor:
chore:
```

Examples:

```text
feat: add jailbreak detector
```

```text
fix: correct RAG retrieval logic
```

```text
security: add PII detection
```

```text
docs: improve Kubernetes security guide
```

---

# ⬆️ 8. Push Your Branch

Push your branch to your fork:

```bash
git push origin feature/prompt-injection-detection
```

Do not push to:

```text
main
```

---

# 🔀 9. Create a Pull Request

Open your fork on GitHub.

GitHub should provide an option to create a Pull Request.

Set:

```text
base repository:
<maintainer-username>/secure-llm

base branch:
main

head repository:
<your-username>/secure-llm

compare branch:
feature/prompt-injection-detection
```

Create the Pull Request.

---

# 🤖 10. CI Checks

After opening the Pull Request, GitHub Actions will automatically run the project's CI pipeline.

The pipeline will eventually perform checks such as:

```text
Pull Request
     ↓
GitHub Actions
     ↓
Build
     ↓
Unit Tests
     ↓
Lint
     ↓
Security Tests
     ↓
Docker Build
     ↓
Trivy Scan
     ↓
Kubernetes Validation
```

A Pull Request should not be merged if required CI checks fail.

---

# 👀 11. Code Review

The maintainer will review your Pull Request.

The maintainer may:

* Approve the PR
* Request changes
* Ask questions
* Request additional tests
* Request security improvements

If changes are requested, update your branch:

```bash
git add .
git commit -m "fix: address review comments"
git push origin feature/prompt-injection-detection
```

The existing Pull Request will automatically update.

---

# ✅ 12. Merge

After:

* CI checks pass
* Required reviews are complete
* Review comments are resolved

the maintainer will merge the Pull Request into `main`.

Contributors should not merge their own Pull Requests unless the project maintainer explicitly allows it.

---

# 🔄 Keeping Your Branch Updated

If the project receives new changes while you are working, update your branch.

First:

```bash
git checkout main
git pull upstream main
```

Then return to your feature branch:

```bash
git checkout feature/prompt-injection-detection
```

Update it:

```bash
git merge main
```

Resolve any conflicts if necessary.

Then:

```bash
git push origin feature/prompt-injection-detection
```

---

# 🚫 What Contributors Should NOT Do

Do not:

* Push directly to `main`
* Force push to `main`
* Commit API keys
* Commit passwords
* Commit Kubernetes Secrets containing real credentials
* Disable security checks to make CI pass
* Submit unrelated changes in one PR
* Copy code without respecting its license
* Remove security tests without justification

---

# 🔒 Security Contributions

Security-related contributions are especially welcome.

Examples:

```text
Prompt Injection
Jailbreak Detection
PII Detection
RAG Poisoning
LLM Output Security
Tool Authorization
Rate Limiting
Kubernetes Security
Container Security
```

When contributing a security feature, include tests demonstrating:

```text
Attack
  ↓
Detection
  ↓
Risk Score
  ↓
Policy
  ↓
Expected Action
```

For example:

```text
Malicious Prompt
       ↓
Prompt Injection Detector
       ↓
Risk = 85
       ↓
Policy Threshold = 70
       ↓
BLOCK
```

---

# 🧪 Adding Security Tests

Security features should include tests whenever possible.

Example:

```text
tests/
    prompt-injection/
    jailbreak/
    pii/
    rag-poisoning/
```

Tests should cover both:

### Malicious Input

```text
Expected → BLOCK
```

### Safe Input

```text
Expected → ALLOW
```

This helps prevent security regressions.

---

# 📝 Pull Request Guidelines

A good Pull Request should clearly explain:

### What changed?

Example:

```text
Added a prompt injection detection module.
```

### Why was it changed?

Example:

```text
This protects the LLM from common instruction override attacks.
```

### How was it tested?

Example:

```text
Added unit tests for malicious and safe prompts.
```

### Security impact

Example:

```text
Requests with risk scores above the configured threshold are blocked.
```

---

# 📋 Pull Request Checklist

Before submitting a Pull Request, check:

* [ ] Code is formatted
* [ ] Tests pass locally
* [ ] New functionality has tests
* [ ] No secrets are committed
* [ ] No unnecessary files are included
* [ ] Documentation is updated if necessary
* [ ] Security implications have been considered
* [ ] Commit messages are meaningful
* [ ] CI checks pass
* [ ] PR description explains the change

---

# 🏗️ Maintainer Workflow

The maintainer should follow:

```text
Pull Request
     ↓
Automated CI
     ↓
Security Checks
     ↓
Code Review
     ↓
Requested Changes
     ↓
Contributor Updates PR
     ↓
CI Runs Again
     ↓
Approval
     ↓
Merge
```

The `main` branch should always remain stable.

---

# 🌟 Good First Contributions

If you are new to the project, consider starting with:

* Documentation improvements
* Unit tests
* Prompt injection test cases
* API improvements
* Logging improvements
* Kubernetes manifest improvements
* Security policy examples
* Monitoring dashboards

Look for issues labeled:

```text
good first issue
help wanted
documentation
security
kubernetes
```

---

# 🤝 Code of Conduct

All contributors are expected to communicate respectfully and constructively.

The goal of SecureLLM is to create a collaborative environment where developers, security researchers, AI engineers, and Kubernetes enthusiasts can learn and build together.

---

# 💡 Questions

If you are unsure about an implementation:

1. Check the documentation.
2. Check existing issues and Pull Requests.
3. Open a GitHub issue.
4. Discuss the proposed approach before making large changes.

For large architectural changes, please open an issue first so the design can be discussed before implementation.

---

# 🚀 Thank You

Every contribution helps improve SecureLLM.

Whether you contribute code, tests, security research, documentation, Kubernetes improvements, or ideas, your contribution is valuable.

**Build secure AI. Build cloud-native. Build together.**
