"""Pydantic schemas for website monitor agent API."""

from datetime import datetime

from pydantic import BaseModel


class MonitorRequest(BaseModel):
    merchant_id: str
    url: str
    alert_threshold_pct: float = 5.0


class MonitorResult(BaseModel):
    merchant_id: str
    action: str
    diff_pct: float
    alert: bool
    screenshot_url: str | None = None
    diff_url: str | None = None


class SnapshotResponse(BaseModel):
    id: str
    merchant_id: str
    screenshot_url: str
    diff_url: str | None
    diff_pct: float
    alert_triggered: bool
    created_at: datetime

    model_config = {"from_attributes": True}
