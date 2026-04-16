"""Integration tests for Braslina API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "service": "braslina"}


@pytest.mark.asyncio
async def test_create_merchant(client):
    payload = {
        "merchant_id": "mrc_test_001",
        "company_name": "Test Corp",
        "website_url": "https://example.com",
        "mcc_code": "5815",
        "contact_email": "test@example.com",
    }
    r = await client.post("/api/v1/onboarding/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["merchant_id"] == "mrc_test_001"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_merchants(client):
    r = await client.get("/api/v1/onboarding/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_create_checklist(client):
    payload = {"merchant_id": "mrc_test_001", "template_id": "tpl_sales_v1"}
    r = await client.post("/api/v1/checklist/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["merchant_id"] == "mrc_test_001"
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_create_test_purchase(client):
    payload = {
        "merchant_id": "mrc_test_001",
        "amount": 1.00,
        "currency": "EUR",
        "card_type": "visa",
    }
    r = await client.post("/api/v1/test-purchase/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["merchant_id"] == "mrc_test_001"


@pytest.mark.asyncio
async def test_get_snapshots(client):
    r = await client.get("/api/v1/monitor/snapshots/mrc_test_001")
    assert r.status_code == 200
