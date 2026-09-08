from pathlib import Path
import sys

import pytest


API_GATEWAY_DIR = Path(__file__).resolve().parents[1] / "api-gateway"
sys.path.insert(0, str(API_GATEWAY_DIR))


LABELS = (
	"prompt injection",
	"jailbreak attempt",
	"PII or sensitive information",
	"system prompt leakage",
	"toxic or abusive content",
	"malicious intent",
	"safe prompt",
)


def fake_classify_prompt(message: str) -> dict:
	message = message.lower()
	scores = {label: 0.05 for label in LABELS}
	scores["safe prompt"] = 0.95

	if "ignore" in message or "previous" in message:
		scores["prompt injection"] = 0.95
	if "unrestricted" in message or "safety rules" in message or "developer mode" in message:
		scores["jailbreak attempt"] = 0.95
	if any(term in message for term in ("@", "phone", "aadhaar", "pan", "card number", "192.168")):
		scores["PII or sensitive information"] = 0.95
	if "system prompt" in message or "instructions" in message:
		scores["system prompt leakage"] = 0.95
	if any(term in message for term in ("worthless", "hate you", "go die", "stupid")):
		scores["toxic or abusive content"] = 0.95
	if any(term in message for term in ("authentication", "ransomware", "phishing", "malware")):
		scores["malicious intent"] = 0.95

	return scores


@pytest.fixture(autouse=True)
def mock_security_classifier(monkeypatch):
	from app.security import analyzer, jailbreak, maliciousintent, pii
	from app.security import prompt_injection, promptleakage, toxicity

	detector_modules = (
		analyzer,
		jailbreak,
		maliciousintent,
		pii,
		prompt_injection,
		promptleakage,
		toxicity,
	)

	for module in detector_modules:
		monkeypatch.setattr(module, "classify_prompt", fake_classify_prompt)