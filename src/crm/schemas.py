"""Pydantic schemas for CRM workflow and reminders."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class WorkflowCreate(BaseModel):
    merchant_id: str
    assignee_id: str | None = None
    notes: dict | None = None
    due_date: datetime | None = None


class WorkflowAdvance(BaseModel):
    new_stage: str
    assignee_id: str | None = None


class WorkflowResponse(BaseModel):
    id: str
    merchant_id: str
    stage: str
    assignee_id: str | None
    notes: dict | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReminderCreate(BaseModel):
    merchant_id: str
    message: str
    scheduled_at: datetime
    channel: Literal["log", "email", "slack"] = "log"


class ReminderResponse(BaseModel):
    id: str
    merchant_id: str
    message: str
    scheduled_at: datetime
    sent_at: datetime | None
    channel: str
    created_at: datetime

    model_config = {"from_attributes": True}
