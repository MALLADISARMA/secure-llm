from app.security import aiclassifier


def test_classifier_uses_pytorch_backend(monkeypatch):
    calls = []

    def fake_pipeline(*args, **kwargs):
        calls.append((args, kwargs))
        return object()

    aiclassifier.get_classifier.cache_clear()
    monkeypatch.setattr(aiclassifier, "pipeline", fake_pipeline)

    classifier = aiclassifier.get_classifier()

    assert classifier is not None
    assert calls == [
        (
            ("zero-shot-classification",),
            {"model": aiclassifier.MODEL_NAME, "framework": "pt"},
        )
    ]