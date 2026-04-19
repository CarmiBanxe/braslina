"""API key authentication middleware."""
from typing import Annotated

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from src.common.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(
    api_key: Annotated[str | None, Security(API_KEY_HEADER)],
) -> str:
    """Validate X-API-Key. Dev bypass only when APP_ENV != production AND key empty."""
    expected = settings.BRASLINA_API_KEY
    if not expected:
        if settings.APP_ENV == "production":
            raise HTTPException(
                status_code=500,
                detail="BRASLINA_API_KEY not configured in production",
            )
        return "dev"
    if not api_key or api_key != expected:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
