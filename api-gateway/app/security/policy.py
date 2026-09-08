from app.security.analyzer import analyze_prompt


def is_unsafe_message(message: str) -> bool:
    """Return True when the central analyzer flags any security category."""
    return analyze_prompt(message)["blocked"]