"""
AI-based toxicity detection.
"""

from app.security.aiclassifier import classify_prompt


THRESHOLD = 0.70


def detect_toxicity(message: str) -> bool:
    """
    Semantically detect toxic, abusive, hateful,
    or threatening content.
    """

    scores = classify_prompt(message)

    return scores["toxic or abusive content"] >= THRESHOLD