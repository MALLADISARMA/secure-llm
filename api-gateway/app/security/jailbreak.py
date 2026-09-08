"""
AI-based jailbreak detection.
"""

from app.security.aiclassifier import classify_prompt


THRESHOLD = 0.70


def detect_jailbreak(message: str) -> bool:
    """
    Semantically detect attempts to bypass model safety
    or behavioral restrictions.
    """

    scores = classify_prompt(message)

    return scores["jailbreak attempt"] >= THRESHOLD