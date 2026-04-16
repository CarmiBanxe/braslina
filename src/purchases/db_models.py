"""SQLAlchemy ORM models for test purchases."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.common.base import Base


class TestPurchaseDB(Base):
    __tablename__ = "test_purchases"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"tp_{uuid.uuid4().hex[:8]}")
    merchant_id: Mapped[str] = mapped_column(String(64), ForeignKey("merchants.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    performed_by: Mapped[str] = mapped_column(String(128), nullable=False)
    performed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    screenshot_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    refund_tested: Mapped[bool] = mapped_column(Boolean, default=False)
    refund_screenshot_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
