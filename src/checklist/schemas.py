"""Pydantic schemas for checklist API."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class CheckStatusEnum(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"
    NOT_APPLICABLE = "not_applicable"


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
    status: CheckStatusEnum
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


class EvaluationResponse(BaseModel):
    total: int
    passed: int
    failed: int
    needs_review: int
    pending: int
    not_applicable: int
    is_complete: bool
    is_blocked: bool
    completion_pct: float
