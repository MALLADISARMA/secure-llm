"""
Common security analysis result models.
"""

from dataclasses import dataclass


@dataclass
class SecurityResult:
    category: str
    detected: bool
    confidence: float
    severity: str