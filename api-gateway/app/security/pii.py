"""
AI-based PII / sensitive information detection.
"""

from app.security.aiclassifier import classify_prompt


THRESHOLD = 0.70


def detect_pii(message: str) -> bool:
    """
    Semantically detect prompts containing or requesting
    personally identifiable or sensitive information.
    """

    scores = classify_prompt(message)

    return scores["PII or sensitive information"] >= THRESHOLD