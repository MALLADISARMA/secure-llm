# Security analysis

## What the checks mean

The gateway evaluates each submitted prompt against six security categories.
These are broad semantic signals, not guarantees that a prompt is safe or
unsafe.

| Category | Plain-language definition | Example of what the check is intended to identify |
| --- | --- | --- |
| Prompt Injection | Instructions in user-provided text that try to override or manipulate the instructions the AI should follow. | Asking the system to ignore earlier instructions or treat supplied text as higher-priority instructions. |
| Jailbreak | Attempts to bypass a model's safety rules or restrictions. | Asking the model to disregard safeguards so it will answer a request it would otherwise refuse. |
| PII / Sensitive Data | Personally identifiable information (PII) is information that can identify or help identify a person, such as a name combined with contact details or an ID number. The broader category also covers other sensitive information. | A prompt containing or asking to expose personal details, credentials, or other sensitive data. This is semantic classification, not a dedicated PII extractor or redactor. |
| System Prompt Leakage | Requests to reveal hidden system or developer instructions, or secrets that should not be disclosed. | Asking the assistant to print its hidden instructions, passwords, API keys, or tokens. |
| Toxicity | Abusive, hateful, or otherwise toxic language. | Insults or abusive language directed at a person or group. |
| Malicious Intent | Requests that appear to seek assistance with harmful or abusive activity. | Asking for instructions to harm someone or misuse a system. |

These descriptions explain the intended categories; they are not exhaustive
rules. The application does not implement a separate rule list for every
example above.

## The classifier model

The security classifier is `facebook/bart-large-mnli`, loaded with the
Hugging Face Transformers `zero-shot-classification` pipeline and PyTorch.
BART is a sequence-to-sequence language model, and the `-mnli` checkpoint is
fine-tuned for Multi-Genre Natural Language Inference (MNLI). Inference lets
the pipeline compare the meaning of the prompt with natural-language category
labels without requiring a separately trained classifier head for each
SecureLLM category.

This fits the project's prototype because it can score several broad
categories, including paraphrased wording, without maintaining a large list
of trigger phrases or training a custom model for each category. It is not
fine-tuned in this repository on a SecureLLM dataset, and its scores are not
an accuracy guarantee.

On the first non-empty prompt, Transformers loads the model into the gateway
process (downloading it if it is not already available in the environment).
The shared pipeline is cached in that process and reused for later prompts.
The model runs as part of the gateway; this is not a call to a hosted model
inference API.

## How scoring and blocking work

The classifier evaluates each prompt against these candidate labels:

| Category | Label passed to classifier | Severity when detected |
| --- | --- | --- |
| Prompt Injection | `prompt injection` | HIGH |
| Jailbreak | `jailbreak attempt` | CRITICAL |
| PII / Sensitive Data | `PII or sensitive information` | HIGH |
| System Prompt Leakage | `system prompt leakage` | HIGH |
| Toxicity | `toxic or abusive content` | MEDIUM |
| Malicious Intent | `malicious intent` | CRITICAL |

It also scores `safe prompt`. The pipeline uses `multi_label=True`, so each
label receives an independent score; a prompt can score highly in more than
one category. The safe-label score is not included in the API's six-category
results and does not determine the block decision.

Each security category is marked detected at a score of **0.70 or greater**.
If any category reaches that threshold, the gateway returns `blocked`;
otherwise it returns `allowed`. Two explicit pattern checks supplement the
model: matching “ignore [all] previous instructions” raises the
prompt-injection score to at least `1.0`, while matching a request to reveal
certain secret-related terms raises the system-prompt-leakage score to at
least `1.0`. These checks do not replace the classifier.

The `overall_score` is the highest of the six security-category scores,
expressed as a percentage. `highest_risk` names the category with that score.
These scores are model outputs, not calibrated probabilities of harm.

## How this relates to generated answers

The security classifier is not the model that writes chat answers. In the
provided browser flow, an allowed prompt is sent separately to the optional
LLM service, which uses Ollama and `qwen2.5:1.5b` by default. A blocked prompt
is not forwarded by that UI flow. The gateway's decision is not an enforcement
proxy for other clients that can access the generation service directly.

## Response interpretation and limitations

Each result contains a category name, a boolean `detected` value, a confidence
rounded to four decimal places, and a severity. Undetected categories use
severity `NONE`. A blocked response includes the analysis object and a generic
blocking reason; it does not include a generated model response.

False positives and false negatives are possible. PII may be missed or
ordinary text may be classified as sensitive; this model does not extract,
mask, or guarantee protection of personal data. Classification depends on the
model, input phrasing, and threshold. Test it against your own threat model
and use independent controls for any consequential application.
