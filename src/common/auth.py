"""API key authentication middleware."""
import os
from typing import Annotated

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(
    api_key: Annotated[str | None, Security(API_KEY_HEADER)]
) -> str:
    """Dependency that validates the X-API-Key header."""
    expected = os.getenv("BRASLINA_API_KEY", "")
    if not expected:
        return "dev"
    if not api_key or api_key != expected:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
