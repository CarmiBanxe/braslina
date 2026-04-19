"""Integration tests for Braslina API endpoints."""
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://braslina:braslina_dev@localhost:5432/braslina",
)

test_engine = create_async_engine(TEST_DB_URL, echo=False, pool_size=5, max_overflow=0)
TestSession = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_app():
    from src.common.base import Base
    from src.common.database import get_db
    from src.main import app

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest_asyncio.fixture
async def client():
    from src.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def merchant_id(client):
    """Create a merchant and return its ID for dependent tests."""
    payload = {
        "name": "FK Test Corp",
        "website": "https://fk-test.com",
        "mcc": "5815",
    }
    r = await client.post("/api/v1/onboarding/", json=payload)
    assert r.status_code == 201
    return r.json()["id"]


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert data["db"] == "ok"


@pytest.mark.asyncio
async def test_create_merchant(client):
    payload = {
        "name": "Test Corp",
        "website": "https://example.com",
        "mcc": "5815",
    }
    r = await client.post("/api/v1/onboarding/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Test Corp"
    assert data["status"] == "new"


@pytest.mark.asyncio
async def test_list_merchants(client):
    r = await client.get("/api/v1/onboarding/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_create_checklist(client, merchant_id):
    payload = {"merchant_id": merchant_id, "template_id": "tpl_sales_v1"}
    r = await client.post("/api/v1/checklist/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["merchant_id"] == merchant_id
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_create_test_purchase(client, merchant_id):
    payload = {
        "merchant_id": merchant_id,
        "amount": 1.00,
        "currency": "EUR",
        "result": "passed",
        "performed_by": "qa@test",
    }
    r = await client.post("/api/v1/test-purchase/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["merchant_id"] == merchant_id


@pytest.mark.asyncio
async def test_get_snapshots(client):
    r = await client.get("/api/v1/monitor/snapshots/mrc_test_001")
    assert r.status_code == 200
