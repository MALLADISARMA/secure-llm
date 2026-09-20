from redis.exceptions import ConnectionError as RedisConnectionError

from app.history import HISTORY_TTL_SECONDS, MAX_HISTORY_RECORDS, HistoryService


class FakeRedis:
    def __init__(self):
        self.data = {}
        self.ttls = {}

    def lpush(self, key, value):
        self.data.setdefault(key, []).insert(0, value)

    def ltrim(self, key, start, end):
        self.data[key] = self.data.get(key, [])[start : end + 1]

    def expire(self, key, ttl):
        self.ttls[key] = ttl

    def lrange(self, key, start, end):
        return self.data.get(key, [])[start : end + 1]

    def delete(self, key):
        self.data.pop(key, None)
        self.ttls.pop(key, None)


def make_analysis(allowed=True):
    return {
        "allowed": allowed,
        "blocked": not allowed,
        "overall_score": 5.0 if allowed else 95.0,
        "highest_risk": "Prompt Injection",
        "results": [],
    }


def test_history_is_saved_and_read_newest_first():
    service = HistoryService(client=FakeRedis())

    first = service.save("session-one", "first", "allowed", make_analysis())
    second = service.save(
        "session-one",
        "second",
        "blocked",
        make_analysis(False),
    )

    records = service.get("session-one")

    assert records[0]["id"] == second["id"]
    assert records[1]["id"] == first["id"]


def test_history_is_session_specific_and_delete_is_scoped():
    client = FakeRedis()
    service = HistoryService(client=client)
    service.save("session-one", "one", "allowed", make_analysis())
    service.save("session-two", "two", "allowed", make_analysis())

    service.delete("session-one")

    assert service.get("session-one") == []
    assert service.get("session-two")[0]["prompt"] == "two"


def test_history_is_limited_and_expiring():
    client = FakeRedis()
    service = HistoryService(client=client)

    for index in range(MAX_HISTORY_RECORDS + 10):
        service.save("session-one", f"prompt-{index}", "allowed", make_analysis())

    records = service.get("session-one")

    assert len(records) == MAX_HISTORY_RECORDS
    assert records[0]["prompt"] == "prompt-59"
    assert client.ttls["securellm:history:session-one"] == HISTORY_TTL_SECONDS


def test_invalid_session_id_is_rejected():
    service = HistoryService(client=FakeRedis())

    for session_id in ("", "session with spaces", "session/other", "a" * 129):
        try:
            service.get(session_id)
        except ValueError:
            continue
        raise AssertionError("Expected invalid session ID to be rejected")


def test_redis_unavailable_returns_none_for_save():
    class UnavailableRedis:
        def lpush(self, *args):
            raise RedisConnectionError("Redis unavailable")

    service = HistoryService(client=UnavailableRedis())

    assert service.save("session-one", "prompt", "allowed", make_analysis()) is None