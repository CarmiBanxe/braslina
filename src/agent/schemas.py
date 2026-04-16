"""Pydantic schemas for website monitor agent API."""

from pydantic import BaseModel
from datetime import datetime


class MonitorRequest(BaseModel):
    merchant_id: str
    url: str
    alert_threshold_pct: float = 5.0


class SnapshotResponse(BaseModel):
    id: str
    merchant_id: str
    screenshot_url: str
    diff_url: str | None
    diff_pct: float | None
    alert_triggered: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MonitorResult(BaseModel):
    merchant_id: str
    action: str | None = None
    diff_pct: float | None = None
    alert: bool = False
    screenshot_url: str | None = None
    diff_url: str | None = None
