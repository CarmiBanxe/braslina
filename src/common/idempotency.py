"""Idempotency key support for POST endpoints."""
import json
import os

import redis.asyncio as aioredis
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
IDEMPOTENCY_TTL = int(os.getenv("BRASLINA_IDEMPOTENCY_TTL", "86400"))

_redis: aioredis.Redis | None = None


async def _get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis


class IdempotencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method != "POST":
            return await call_next(request)
        idem_key = request.headers.get("X-Idempotency-Key")
        if not idem_key:
            return await call_next(request)
        r = await _get_redis()
        cache_key = f"braslina:idempotency:{idem_key}"
        cached = await r.get(cache_key)
        if cached:
            data = json.loads(cached)
            return Response(
                content=data["body"],
                status_code=data["status_code"],
                media_type="application/json",
            )
        response = await call_next(request)
        body = b""
        async for chunk in response.body_iterator:
            body += chunk if isinstance(chunk, bytes) else chunk.encode()
        await r.setex(
            cache_key,
            IDEMPOTENCY_TTL,
            json.dumps({"body": body.decode(), "status_code": response.status_code}),
        )
        return Response(
            content=body,
            status_code=response.status_code,
            media_type=response.media_type,
            headers=dict(response.headers),
        )
