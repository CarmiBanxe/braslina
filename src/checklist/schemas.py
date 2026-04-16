"""Pydantic schemas for checklist API."""

from datetime import datetime

from pydantic import BaseModel


class CheckItemResponse(BaseModel):
    id: str
    name: str
    description: str
    auto_verifiable: bool
    status: str
    verified_at: datetime | None
    evidence_url: str | None
    notes: str | None

    model_config = {"from_attributes": True}


class ChecklistCreate(BaseModel):
    merchant_id: str
    template_id: str = "tpl_sales_v1"


class CheckItemUpdate(BaseModel):
    status: str
    evidence_url: str | None = None
    notes: str | None = None


class ChecklistResponse(BaseModel):
    id: str
    merchant_id: str
    template_id: str
    created_at: datetime
    completed_at: datetime | None
    items: list[CheckItemResponse] = []

    model_config = {"from_attributes": True}
