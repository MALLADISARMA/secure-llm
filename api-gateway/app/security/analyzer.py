"""
Central security analyzer.

Runs AI-based semantic classification against all
six security categories.
"""

from app.security.aiclassifier import classify_prompt
from app.security.result import SecurityResult


THRESHOLD = 0.70


CATEGORY_CONFIG = {
    "Prompt Injection": {
        "model_label": "prompt injection",
        "severity": "HIGH",
    },
    "Jailbreak": {
        "model_label": "jailbreak attempt",
        "severity": "CRITICAL",
    },
    "PII / Sensitive Data": {
        "model_label": "PII or sensitive information",
        "severity": "HIGH",
    },
    "System Prompt Leakage": {
        "model_label": "system prompt leakage",
        "severity": "HIGH",
    },
    "Toxicity": {
        "model_label": "toxic or abusive content",
        "severity": "MEDIUM",
    },
    "Malicious Intent": {
        "model_label": "malicious intent",
        "severity": "CRITICAL",
    },
}


def analyze_prompt(message: str) -> dict:
    """
    Analyze a prompt across all six security categories.
    """

    scores = classify_prompt(message)

    results = []

    for category, config in CATEGORY_CONFIG.items():

        confidence = scores[config["model_label"]]

        detected = confidence >= THRESHOLD

        results.append(
            SecurityResult(
                category=category,
                detected=detected,
                confidence=round(confidence, 4),
                severity=config["severity"] if detected else "NONE",
            )
        )

    blocked = any(result.detected for result in results)

    highest_risk = max(
        results,
        key=lambda result: result.confidence,
    )

    overall_score = round(
        highest_risk.confidence * 100,
        2,
    )

    return {
        "allowed": not blocked,
        "blocked": blocked,
        "overall_score": overall_score,
        "highest_risk": highest_risk.category,
        "results": [
            {
                "category": result.category,
                "detected": result.detected,
                "confidence": result.confidence,
                "severity": result.severity,
            }
            for result in results
        ],
    }