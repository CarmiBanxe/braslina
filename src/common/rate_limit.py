"""Redis-backed rate limiter."""
import os
from fastapi import HTTPException, Request
import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RATE_LIMIT = int(os.getenv("BRASLINA_RATE_LIMIT", "100"))
RATE_WINDOW = int(os.getenv("BRASLINA_RATE_WINDOW", "60"))

_redis: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis


async def rate_limit_check(request: Request) -> None:
    """Check rate limit for the requesting IP. Raises 429 if exceeded."""
    r = await get_redis()
    client_ip = request.client.host if request.client else "unknown"
    key = f"braslina:ratelimit:{client_ip}"
    current = await r.incr(key)
    if current == 1:
        await r.expire(key, RATE_WINDOW)
    if current > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT} requests per {RATE_WINDOW}s.",
        )
