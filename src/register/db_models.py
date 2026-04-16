"""SQLAlchemy ORM models for merchant register."""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base


class MerchantStatus(StrEnum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


VALID_STATUS_TRANSITIONS: dict[MerchantStatus, set[MerchantStatus]] = {
    MerchantStatus.NEW: {MerchantStatus.UNDER_REVIEW},
    MerchantStatus.UNDER_REVIEW: {MerchantStatus.APPROVED, MerchantStatus.REJECTED},
    MerchantStatus.APPROVED: {MerchantStatus.SUSPENDED},
    MerchantStatus.REJECTED: {MerchantStatus.UNDER_REVIEW},
    MerchantStatus.SUSPENDED: {MerchantStatus.UNDER_REVIEW},
}


class MerchantDB(Base):
    __tablename__ = "merchants"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"mer_{uuid.uuid4().hex[:8]}")
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str] = mapped_column(String(1024), nullable=False)
    mcc: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=MerchantStatus.NEW.value)
    assigned_owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    status_log: Mapped[list["MerchantStatusLogDB"]] = relationship(
        back_populates="merchant", cascade="all, delete-orphan", order_by="MerchantStatusLogDB.changed_at"
    )


class MerchantStatusLogDB(Base):
    __tablename__ = "merchant_status_log"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"msl_{uuid.uuid4().hex[:8]}")
    merchant_id: Mapped[str] = mapped_column(String(64), ForeignKey("merchants.id"), nullable=False)
    from_status: Mapped[str] = mapped_column(String(32), nullable=False)
    to_status: Mapped[str] = mapped_column(String(32), nullable=False)
    changed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    merchant: Mapped["MerchantDB"] = relationship(back_populates="status_log")
