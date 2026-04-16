"""Pydantic schemas for test purchases API."""

from datetime import datetime

from pydantic import BaseModel


class PurchaseCreate(BaseModel):
    merchant_id: str
    amount: float
    currency: str = "EUR"
    result: str
    performed_by: str
    screenshot_url: str | None = None
    refund_tested: bool = False
    refund_screenshot_url: str | None = None
    notes: str | None = None


class PurchaseResponse(BaseModel):
    id: str
    merchant_id: str
    amount: float
    currency: str
    result: str
    performed_by: str
    performed_at: datetime
    screenshot_url: str | None
    refund_tested: bool
    refund_screenshot_url: str | None
    notes: str | None

    model_config = {"from_attributes": True}
