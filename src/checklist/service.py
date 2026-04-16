"""Checklist service — business logic layer."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.checklist.db_models import CheckItemDB, ChecklistDB
from src.checklist.engine import (
    CheckStatus,
    EvaluationResult,
    evaluate,
    is_valid_transition,
    load_template,
)
from src.checklist.repository import ChecklistRepository
from src.common.exceptions import InvalidStateTransition, NotFoundError


class ChecklistService:
    def __init__(self, db: AsyncSession):
        self.repo = ChecklistRepository(db)

    async def create_from_template(self, merchant_id: str, template_id: str = "tpl_sales_v1") -> ChecklistDB:
        template = load_template(template_id)
        checklist = ChecklistDB(merchant_id=merchant_id, template_id=template_id)
        for item in template.items:
            checklist.items.append(
                CheckItemDB(
                    name=item.label,
                    description=item.code,
                    auto_verifiable=item.auto_verifiable,
                    status=CheckStatus.PENDING.value,
                )
            )
        return await self.repo.create(checklist)

    async def get_checklist(self, checklist_id: str) -> ChecklistDB:
        checklist = await self.repo.get_by_id(checklist_id)
        if not checklist:
            raise NotFoundError("Checklist", checklist_id)
        return checklist

    async def list_by_merchant(self, merchant_id: str) -> list[ChecklistDB]:
        return await self.repo.list_by_merchant(merchant_id)

    async def update_item_status(
        self, item_id: str, new_status: str, evidence_url: str | None = None, notes: str | None = None
    ) -> CheckItemDB:
        item = await self.repo.get_item(item_id)
        if not item:
            raise NotFoundError("CheckItem", item_id)
        if not is_valid_transition(item.status, new_status):
            raise InvalidStateTransition("CheckItem", item.status, new_status)
        item.status = new_status
        item.verified_at = datetime.now(UTC)
        if evidence_url is not None:
            item.evidence_url = evidence_url
        if notes is not None:
            item.notes = notes
        return await self.repo.update_item(item)

    async def evaluate_checklist(self, checklist_id: str) -> EvaluationResult:
        checklist = await self.get_checklist(checklist_id)
        statuses = [item.status for item in checklist.items]
        result = evaluate(statuses)
        if result.is_complete:
            checklist.completed_at = datetime.now(UTC)
            await self.repo.update_item(checklist)  # just commit
        return result
