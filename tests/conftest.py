"""Shared test fixtures for braslina."""
import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

os.environ.setdefault("BRASLINA_API_KEY", "")
os.environ.setdefault("BRASLINA_ENV", "test")

from src.common.base import Base
from src.common.database import get_db
from src.main import app

TEST_DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://braslina:braslina_dev@localhost:5432/braslina",
)

# NullPool: each DB call gets a fresh connection in whatever event loop is running.
# This prevents "Future attached to a different loop" errors when session-scoped setup_db
# (runs in session loop) and function-scoped tests (run in per-test loops) share the engine.
engine = create_async_engine(TEST_DB_URL, echo=False, poolclass=NullPool)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSession() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def _override_session() -> AsyncGenerator[AsyncSession, None]:
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = _override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
