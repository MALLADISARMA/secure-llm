"""
AI-based system prompt leakage detection.
"""

from app.security.aiclassifier import classify_prompt


THRESHOLD = 0.70


def detect_prompt_leakage(message: str) -> bool:
    """
    Semantically detect attempts to obtain hidden,
    system, developer, or internal instructions.
    """

    scores = classify_prompt(message)

    return scores["system prompt leakage"] >= THRESHOLD