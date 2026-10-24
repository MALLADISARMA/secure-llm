# Security analysis

## Categories

The gateway scores each prompt against six labels using one shared
zero-shot-classification model:

| Category | Label passed to classifier | Severity when detected |
| --- | --- | --- |
| Prompt Injection | `prompt injection` | HIGH |
| Jailbreak | `jailbreak attempt` | CRITICAL |
| PII / Sensitive Data | `PII or sensitive information` | HIGH |
| System Prompt Leakage | `system prompt leakage` | HIGH |
| Toxicity | `toxic or abusive content` | MEDIUM |
| Malicious Intent | `malicious intent` | CRITICAL |

The classifier also scores a `safe prompt` label. The API response reports the
six security categories, not the safe-label score.

## Scoring and decision

`facebook/bart-large-mnli` is used through the Transformers
zero-shot-classification pipeline with `multi_label=True`. Each security
category has an independent confidence score. A category is marked detected
at a confidence of **0.70 or greater**. If any category is detected, the
gateway returns `blocked`; otherwise it returns `allowed`.

The `overall_score` is the highest of the six security-category confidences,
expressed as a percentage. `highest_risk` names the category with that score.
These values do not represent a calibrated probability of harm.

Two explicit pattern checks can raise a score to `1.0`: a phrase matching
“ignore [all] previous instructions” raises the prompt-injection score, and
requests to reveal certain secret-related terms raise the system-prompt-leakage
score. They supplement the model and do not replace it.

The classifier is cached in process after first load so repeated analysis
requests reuse the same model pipeline.

## Response interpretation

Each result contains a category name, a boolean `detected` value, a confidence
rounded to four decimal places, and a severity. Undetected categories use
severity `NONE`. A blocked response includes the same analysis object and a
generic blocking reason; it does not include a generated model response.

False positives and false negatives are possible. Classification depends on
the model, input phrasing, and threshold. Test it against your own threat model
and use independent controls for any consequential application.
