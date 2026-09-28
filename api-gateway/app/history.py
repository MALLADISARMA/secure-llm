import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

import redis
from redis.exceptions import RedisError


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

HISTORY_PREFIX = "securellm:history:"
MAX_HISTORY_RECORDS = 50
HISTORY_TTL_SECONDS = 7 * 24 * 60 * 60

SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


class HistoryService:
    """
    Redis-backed history service.

    Redis is treated as an optional dependency:
    - Redis failures are handled gracefully.
    - The main security analysis endpoint can continue without Redis.
    """

    def __init__(self, redis_url: str = REDIS_URL, client: Optional[Any] = None):
        self.redis_url = redis_url
        self.client = client

        if self.client is None:
            self.client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )

    @staticmethod
    def validate_session_id(session_id: str) -> str:
        """
        Validate the session ID received from the browser.

        Only UUID-compatible alphanumeric/hyphen/underscore values are
        accepted. This prevents arbitrary Redis key construction.
        """
        if not isinstance(session_id, str):
            raise ValueError("Invalid session ID")

        session_id = session_id.strip()

        if not SESSION_ID_PATTERN.fullmatch(session_id):
            raise ValueError("Invalid session ID")

        return session_id

    @classmethod
    def build_key(cls, session_id: str) -> str:
        """
        Build a Redis key only after validating the session ID.
        """
        validated_session_id = cls.validate_session_id(session_id)
        return f"{HISTORY_PREFIX}{validated_session_id}"

    @staticmethod
    def create_record(
        session_id: str,
        prompt: str,
        status: str,
        analysis: dict,
    ) -> dict:
        """
        Create the normalized history record stored in Redis.
        """
        if status not in {"allowed", "blocked"}:
            raise ValueError("Invalid history status")

        return {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "prompt": prompt,
            "status": status,
            "overall_score": analysis.get("overall_score", 0.0),
            "highest_risk": analysis.get("highest_risk"),
            "analysis": analysis,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def save(
        self,
        session_id: str,
        prompt: str,
        status: str,
        analysis: dict,
    ) -> Optional[dict]:
        """
        Save a history record.

        Returns the saved record when successful.
        Returns None when Redis is unavailable.
        """
        try:
            key = self.build_key(session_id)

            record = self.create_record(
                session_id=session_id,
                prompt=prompt,
                status=status,
                analysis=analysis,
            )

            self.client.lpush(key, json.dumps(record))

            # Keep only the newest 50 records.
            self.client.ltrim(key, 0, MAX_HISTORY_RECORDS - 1)

            # Refresh TTL whenever a new record is written.
            self.client.expire(key, HISTORY_TTL_SECONDS)

            return record

        except RedisError:
            return None

    def get(self, session_id: str) -> Optional[list[dict]]:
        """
        Return history in reverse chronological order.

        Redis LPUSH means index 0 is the newest record.
        """
        key = self.build_key(session_id)

        try:

            raw_records = self.client.lrange(
                key,
                0,
                MAX_HISTORY_RECORDS - 1,
            )

            return [json.loads(record) for record in raw_records]

        except RedisError:
            return None

        except (ValueError, TypeError):
            # A malformed stored record should not crash the endpoint.
            return []

    def delete(self, session_id: str) -> Optional[bool]:
        """
        Delete only the current session's history.
        """
        try:
            key = self.build_key(session_id)
            self.client.delete(key)
            return True

        except RedisError:
            return None

    def ping(self) -> bool:
        """
        Check Redis availability.
        """
        try:
            return bool(self.client.ping())
        except RedisError:
            return False