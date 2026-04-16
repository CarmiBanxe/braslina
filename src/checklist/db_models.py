"""SQLAlchemy ORM models for checklists."""

import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base


class ChecklistDB(Base):
    __tablename__ = "checklists"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"mcl_{uuid.uuid4().hex[:8]}")
    merchant_id: Mapped[str] = mapped_column(String(64), ForeignKey("merchants.id"), nullable=False)
    template_id: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    items: Mapped[list["CheckItemDB"]] = relationship(back_populates="checklist", cascade="all, delete-orphan")


class CheckItemDB(Base):
    __tablename__ = "check_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: f"chi_{uuid.uuid4().hex[:8]}")
    checklist_id: Mapped[str] = mapped_column(String(64), ForeignKey("checklists.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    auto_verifiable: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(16), default="pending")
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    evidence_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    checklist: Mapped["ChecklistDB"] = relationship(back_populates="items")
