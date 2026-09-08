"""
Shared AI-based security classifier.

Uses a zero-shot classification model to semantically classify
user prompts into security categories.
"""

from functools import lru_cache

from transformers import pipeline


MODEL_NAME = "facebook/bart-large-mnli"

SECURITY_LABELS = [
    "prompt injection",
    "jailbreak attempt",
    "PII or sensitive information",
    "system prompt leakage",
    "toxic or abusive content",
    "malicious intent",
    "safe prompt",
]


@lru_cache(maxsize=1)
def get_classifier():
    """
    Load the classification model only once.

    The model is cached so every detector does not load its
    own copy of the model.
    """

    return pipeline(
        "zero-shot-classification",
        model=MODEL_NAME,
        framework="pt",
    )


def classify_prompt(message: str) -> dict:
    """
    Classify a prompt against all security categories.

    Returns the highest confidence score for each category.
    """

    if not message or not message.strip():
        return {
            "prompt injection": 0.0,
            "jailbreak attempt": 0.0,
            "PII or sensitive information": 0.0,
            "system prompt leakage": 0.0,
            "toxic or abusive content": 0.0,
            "malicious intent": 0.0,
            "safe prompt": 1.0,
        }

    classifier = get_classifier()

    result = classifier(
        message,
        candidate_labels=SECURITY_LABELS,
        multi_label=True,
    )

    scores = dict(zip(result["labels"], result["scores"]))

    return {
        label: scores.get(label, 0.0)
        for label in SECURITY_LABELS
    }