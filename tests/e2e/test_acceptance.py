"""E2E acceptance test: full onboarding scenario."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_onboarding_scenario(client: AsyncClient):
    """Complete merchant onboarding from creation to approval."""

    merchant_data = {
        "name": "E2E Test Corp",
        "website": "https://e2e-test.example.com",
        "mcc": "5815",
    }
    resp = await client.post("/api/v1/onboarding/", json=merchant_data)
    assert resp.status_code in (200, 201), f"Create failed: {resp.text}"
    merchant = resp.json()
    merchant_id = merchant["id"]
    assert merchant["status"] == "new"

    resp = await client.post(f"/api/v1/checklist/evaluate/{merchant_id}")
    assert resp.status_code in (200, 201, 404)

    purchase_data = {
        "merchant_id": str(merchant_id),
        "amount": 9.99,
        "currency": "EUR",
        "result": "passed",
        "performed_by": "e2e@test",
        "performed_by": "e2e@test",
        "notes": "E2E acceptance test purchase",
    }
    resp = await client.post("/api/v1/test-purchase/", json=purchase_data)
    assert resp.status_code in (200, 201), f"Purchase failed: {resp.text}"

    resp = await client.patch(
        f"/api/v1/onboarding/{merchant_id}/status",
        json={"status": "under_review"},
    )
    assert resp.status_code == 200, f"Status change failed: {resp.text}"

    resp = await client.patch(
        f"/api/v1/onboarding/{merchant_id}/status",
        json={"status": "approved"},
    )
    assert resp.status_code == 200, f"Approval failed: {resp.text}"

    resp = await client.get(f"/api/v1/onboarding/{merchant_id}")
    assert resp.status_code == 200, f"Fetch failed: {resp.text}"
    merchant = resp.json()
    assert merchant["status"] == "approved"
