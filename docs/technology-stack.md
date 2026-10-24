# Technology choices

This page describes how the technologies currently in the repository are
used. It explains their fit for this implementation, not a claim that they
are the only suitable choices.

## Frontend

| Technology | Role | Why it fits here |
| --- | --- | --- |
| React 19 | Component-based UI for the dashboard, analyzer, and history | Keeps interactive pages and reusable result components in a familiar component model |
| React Router 7 | Routes for `/`, `/analyzer`, and `/history` | Provides client-side navigation between the three views |
| Vite 8 | Local development server and production asset build | Supplies the frontend dev/build workflow configured by the project |
| Tailwind CSS 3 | Utility-based styling | Lets the UI style components directly without a separate component framework |
| Lucide React | UI icons | Supplies icons used by the dashboard, navigation, and history controls |
| Browser `fetch` and `localStorage` | Calls local APIs and retains the session ID | Avoids an additional client-state or HTTP library for the current request flow |

Frontend dependency declarations live in `frontend/package.json`.

## Gateway and analysis

| Technology | Role | Why it fits here |
| --- | --- | --- |
| Python 3.12+ | Gateway runtime and tests | Runs the API and the Python ML/security integrations |
| FastAPI | HTTP gateway and OpenAPI generation | Maps endpoint functions and Pydantic schemas to an API with interactive docs |
| Pydantic | Request and response validation | Defines API payload constraints and response models |
| Hugging Face Transformers | Loads the zero-shot classifier | Provides the classification pipeline used to score the security categories |
| PyTorch | Model framework | Explicitly selected by the Transformers pipeline |
| `facebook/bart-large-mnli` | Classification model | Supplies the natural-language-inference model used for zero-shot labels |
| pytest and HTTPX | Backend test tooling | Run the project's Python tests and API-level checks |

The model is cached in the gateway process after it is first loaded. The
current implementation is not a remote model API integration.

## Optional storage and generation

| Technology | Role | Why it fits here |
| --- | --- | --- |
| Redis 5–6 | Optional session history storage | Supports a bounded list with expiration without making analysis depend on persistent storage |
| Docker | Packages the LLM service and Redis | Makes the optional local supporting services repeatable to launch |
| Ollama | Local model runtime | Serves the model to the LLM service on the developer machine |
| `qwen2.5:1.5b` | Default generation model | Is the configured default for local response generation |
| Requests | LLM service's HTTP client | Sends a non-streaming generation request to Ollama |

The LLM service is intentionally separate from the gateway. Its Python
dependencies and Dockerfile are under `llm-service/`.

## Repository quality and security scanning

| Technology | Role |
| --- | --- |
| GitHub Actions | Runs tests, syntax checks, frontend lint/build, Trivy, and MkDocs |
| Trivy | Finds filesystem dependency vulnerabilities and produces SARIF output |
| MkDocs Material | Builds and themes this documentation site |

The existing application CI runs Python tests and frontend lint/build. The
documentation workflow uses MkDocs' strict mode to catch broken references
and warnings before a Pages deployment.
