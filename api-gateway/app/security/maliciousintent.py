"""
AI-based malicious intent detection.
"""

from app.security.aiclassifier import classify_prompt


THRESHOLD = 0.70


def detect_malicious_intent(message: str) -> bool:
    """
    Semantically detect potentially harmful or malicious intent.
    """

    scores = classify_prompt(message)

    return scores["malicious intent"] >= THRESHOLD