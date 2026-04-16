"""Pydantic schemas for merchant register API."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class MerchantStatusEnum(StrEnum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class MerchantCreate(BaseModel):
    name: str
    website: str
    mcc: str


class MerchantUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    mcc: str | None = None
    assigned_owner: str | None = None


class StatusChangeRequest(BaseModel):
    status: MerchantStatusEnum
    changed_by: str | None = None
    reason: str | None = None


class StatusLogEntry(BaseModel):
    id: str
    from_status: str
    to_status: str
    changed_by: str | None
    reason: str | None
    changed_at: datetime

    model_config = {"from_attributes": True}


class MerchantResponse(BaseModel):
    id: str
    name: str
    website: str
    mcc: str
    status: str
    assigned_owner: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MerchantDetailResponse(MerchantResponse):
    status_log: list[StatusLogEntry] = []
