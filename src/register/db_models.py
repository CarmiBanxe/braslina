"""SQLAlchemy ORM models for merchant register."""

import uuid
from datetime import date, datetime

from sqlalchemy import String, Float, Date, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.common.base import Base


class MerchantDB(Base):
    __tablename__ = "merchants"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"mrc_{uuid.uuid4().hex[:8]}")
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str] = mapped_column(String(512), nullable=False)
    mcc: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="new")
    date_started_work: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_review_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    monthly_volume: Mapped[float] = mapped_column(Float, default=0.0)
    assigned_to: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
