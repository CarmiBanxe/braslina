"""SQLAlchemy ORM models for website monitoring snapshots."""

import uuid
from datetime import datetime

from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.common.base import Base


class SnapshotDB(Base):
    __tablename__ = "snapshots"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"snap_{uuid.uuid4().hex[:8]}")
    merchant_id: Mapped[str] = mapped_column(String(64), ForeignKey("merchants.id"), nullable=False)
    screenshot_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    diff_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    diff_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    alert_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
