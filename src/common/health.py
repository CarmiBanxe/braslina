"""Health check endpoint with DB, Redis, MinIO status."""
import os

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


async def _check_db() -> str:
    """Check database connectivity."""
    try:
        from sqlalchemy import text
        from src.common.database import async_session
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        return "ok"
    except Exception as e:
        return f"error: {e}"


async def _check_redis() -> str:
    """Check Redis connectivity."""
    try:
        import redis.asyncio as aioredis
        url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        r = aioredis.from_url(url)
        await r.ping()
        await r.aclose()
        return "ok"
    except Exception as e:
        return f"error: {e}"


async def _check_minio() -> str:
    """Check MinIO connectivity."""
    try:
        from minio import Minio
        client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9002"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=False,
        )
        client.list_buckets()
        return "ok"
    except Exception as e:
        return f"error: {e}"


@router.get("/health")
async def health_check():
    """Detailed health check."""
    db = await _check_db()
    redis_status = await _check_redis()
    minio_status = await _check_minio()
    status = "ok" if all(s == "ok" for s in [db, redis_status, minio_status]) else "degraded"
    return {
        "status": status,
        "db": db,
        "redis": redis_status,
        "minio": minio_status,
    }
