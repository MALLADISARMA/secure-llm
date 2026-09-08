"""
AI-based prompt injection detection.
"""

from app.security.aiclassifier import classify_prompt


THRESHOLD = 0.70


def detect_prompt_injection(message: str) -> bool:
    """
    Semantically detect prompt injection attempts.

    The decision is based on an AI classification model,
    not predefined keywords.
    """

    scores = classify_prompt(message)

    return scores["prompt injection"] >= THRESHOLD