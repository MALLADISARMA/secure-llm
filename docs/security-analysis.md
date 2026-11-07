# Security analysis

## Category definitions

The gateway scores each prompt against six broad security categories. These
definitions describe what each check is intended to identify; they are not
exhaustive rules or guarantees.

| Category | Definition | Severity when detected |
| --- | --- | --- |
| Prompt Injection | User-provided text that tries to override, manipulate, or take priority over the instructions an AI system should follow. | HIGH |
| Jailbreak | An attempt to bypass a model's safety rules or restrictions so it will answer a request it would otherwise refuse. | CRITICAL |
| PII / Sensitive Data | Personally identifiable information (PII) is information that identifies or could help identify a person, such as a name with contact details or an ID number. The broader category also includes other sensitive information, such as credentials. | HIGH |
| System Prompt Leakage | An attempt to reveal hidden system or developer instructions, or secrets that should not be disclosed, such as passwords, API keys, or tokens. | HIGH |
| Toxicity | Abusive, hateful, or otherwise toxic language, including language directed at a person or group. | MEDIUM |
| Malicious Intent | A request that appears to seek help with harmful or abusive activity. | CRITICAL |

The PII category is a semantic classification signal. This project does not
use a dedicated PII extraction or redaction engine, and detection does not
guarantee that personal information will be found or removed.

## Model and why it is used

The security model is `facebook/bart-large-mnli`, loaded with the Hugging Face
Transformers `zero-shot-classification` pipeline and PyTorch. The MNLI model
was trained for natural-language inference, which allows the pipeline to
compare a prompt with category labels without training a separate
SecureLLM-specific classifier for every category.

This model lets the prototype evaluate broad categories and varied wording
without relying only on a large list of exact phrases. It has not been
fine-tuned in this repository on a SecureLLM dataset, and model scores are not
an accuracy guarantee. On the first non-empty prompt, Transformers loads the
model into the gateway process (downloading it if it is not already available).
The shared pipeline is cached in that process and reused for subsequent
prompts; the gateway does not call a hosted inference API.

## Scoring and decision

The pipeline compares each prompt with these candidate labels:

| Category | Label passed to classifier |
| --- | --- |
| Prompt Injection | `prompt injection` |
| Jailbreak | `jailbreak attempt` |
| PII / Sensitive Data | `PII or sensitive information` |
| System Prompt Leakage | `system prompt leakage` |
| Toxicity | `toxic or abusive content` |
| Malicious Intent | `malicious intent` |

It also scores `safe prompt`. With `multi_label=True`, each label receives an
independent confidence score, so more than one category may score highly. The
safe-label score is not included in the API's six-category results and does
not decide whether a prompt is blocked.

A category is marked detected at a score of **0.70 or greater**. If any
category reaches this threshold, the gateway returns `blocked`; otherwise it
returns `allowed`. Two explicit pattern checks supplement the model: matching
“ignore [all] previous instructions” raises the prompt-injection score to at
least `1.0`, and matching requests to reveal certain secret-related terms
raises the system-prompt-leakage score to at least `1.0`.

The `overall_score` is the highest of the six security-category scores,
expressed as a percentage. `highest_risk` names the category with that score.
These scores are model outputs, not calibrated probabilities of harm.

## Security model versus response-generation model

`facebook/bart-large-mnli` classifies prompts; it does not write chat answers.
In the browser flow, an allowed prompt is sent separately to the optional
LLM service, which uses Ollama and `qwen2.5:1.5b` by default to generate a
response. A blocked prompt is not forwarded by that UI flow. The gateway is
not an enforcement proxy for other clients that can directly access the
generation service.

## Response interpretation and limitations

Each result contains a category name, a boolean `detected` value, a confidence
rounded to four decimal places, and a severity. Undetected categories use
severity `NONE`. A blocked response includes the analysis object and a generic
blocking reason; it does not include a generated model response.

False positives and false negatives are possible. PII may be missed, or
ordinary text may be classified as sensitive. The classifier does not extract,
mask, or guarantee protection of personal data. Classification depends on the
model, input phrasing, and threshold. Test it against your own threat model
and use independent controls for any consequential application.
