def detect_prompt_injection(message: str) -> bool:
    """
    Basic rule-based prompt injection detection.
    """

    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore your instructions",
        "system prompt",
        "reveal your prompt",
        "jailbreak",
    ]

    message = message.lower()

    for pattern in suspicious_patterns:
        if pattern in message:
            return True

    return False