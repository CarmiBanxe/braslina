"""SQLAlchemy ORM models for CRM workflow and reminders."""
import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from src.common.base import Base


class WorkflowStage(StrEnum):
    NEW = "new"
    SALES_REVIEW = "sales_review"
    COMPLIANCE_REVIEW = "compliance_review"
    CARDS_REVIEW = "cards_review"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


VALID_WORKFLOW_TRANSITIONS: dict[WorkflowStage, set[WorkflowStage]] = {
    WorkflowStage.NEW: {WorkflowStage.SALES_REVIEW},
    WorkflowStage.SALES_REVIEW: {WorkflowStage.COMPLIANCE_REVIEW, WorkflowStage.REJECTED},
    WorkflowStage.COMPLIANCE_REVIEW: {WorkflowStage.CARDS_REVIEW, WorkflowStage.REJECTED},
    WorkflowStage.CARDS_REVIEW: {WorkflowStage.PENDING_APPROVAL, WorkflowStage.REJECTED},
    WorkflowStage.PENDING_APPROVAL: {WorkflowStage.APPROVED, WorkflowStage.REJECTED},
    WorkflowStage.APPROVED: set(),
    WorkflowStage.REJECTED: {WorkflowStage.SALES_REVIEW},
}


class CRMWorkflowDB(Base):
    __tablename__ = "crm_workflows"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"wf_{uuid.uuid4().hex[:8]}")
    merchant_id: Mapped[str] = mapped_column(String(64), ForeignKey("merchants.id"), nullable=False)
    stage: Mapped[str] = mapped_column(String(32), default=WorkflowStage.NEW.value)
    assignee_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class ReminderDB(Base):
    __tablename__ = "reminders"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"rem_{uuid.uuid4().hex[:8]}")
    merchant_id: Mapped[str] = mapped_column(String(64), ForeignKey("merchants.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    channel: Mapped[str] = mapped_column(String(32), default="log")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
