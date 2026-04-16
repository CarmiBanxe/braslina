"""Pydantic schemas for merchant register API."""

from datetime import date, datetime

from pydantic import BaseModel


class MerchantCreate(BaseModel):
    name: str
    website: str
    mcc: str
    status: str = "new"
    date_started_work: date | None = None
    monthly_volume: float = 0.0
    assigned_to: str | None = None
    notes: str | None = None


class MerchantUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    mcc: str | None = None
    status: str | None = None
    date_started_work: date | None = None
    next_review_date: date | None = None
    monthly_volume: float | None = None
    assigned_to: str | None = None
    notes: str | None = None


class MerchantResponse(BaseModel):
    id: str
    name: str
    website: str
    mcc: str
    status: str
    date_started_work: date | None
    next_review_date: date | None
    monthly_volume: float
    assigned_to: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
