"""CRM Integration — n8n webhook triggers for merchant lifecycle events."""

from __future__ import annotations

from typing import Any, cast

import httpx


class N8nWebhookClient:
    """Sends events to self-hosted n8n instance via webhooks."""

    def __init__(self, base_url: str = "http://localhost:5678"):
        self.base_url = base_url.rstrip("/")

    async def trigger(self, webhook_path: str, payload: dict[str, Any]) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{self.base_url}/webhook/{webhook_path}", json=payload
            )
            resp.raise_for_status()
            return cast(dict[str, Any], resp.json())

    async def merchant_created(self, merchant: dict) -> dict:
        return await self.trigger("merchant-created", merchant)

    async def status_changed(self, merchant_id: str, old_status: str, new_status: str) -> dict:
        return await self.trigger("status-changed", {
            "merchant_id": merchant_id,
            "old_status": old_status,
            "new_status": new_status,
        })

    async def monitor_alert(self, merchant_id: str, diff_pct: float, diff_url: str) -> dict:
        return await self.trigger("monitor-alert", {
            "merchant_id": merchant_id,
            "diff_pct": diff_pct,
            "diff_url": diff_url,
        })

    async def checklist_completed(self, merchant_id: str, checklist_id: str) -> dict:
        return await self.trigger("checklist-completed", {
            "merchant_id": merchant_id,
            "checklist_id": checklist_id,
        })

    async def review_reminder(self, merchant_id: str, review_date: str) -> dict:
        return await self.trigger("review-reminder", {
            "merchant_id": merchant_id,
            "review_date": review_date,
        })


if __name__ == "__main__":
    print("N8nWebhookClient ready — 5 webhook triggers defined")
