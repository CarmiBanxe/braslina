"""CRM service — workflow stage transitions and reminder scheduling."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import InvalidStateTransition, NotFoundError
from src.crm.db_models import (
    VALID_WORKFLOW_TRANSITIONS,
    CRMWorkflowDB,
    ReminderDB,
    WorkflowStage,
)
from src.crm.repository import ReminderRepository, WorkflowRepository


class CRMService:
    def __init__(self, db: AsyncSession):
        self.wf_repo = WorkflowRepository(db)
        self.rem_repo = ReminderRepository(db)
        self.db = db

    # --- Workflow ---

    async def create_workflow(
        self,
        merchant_id: str,
        assignee_id: str | None = None,
        notes: dict | None = None,
        due_date: datetime | None = None,
    ) -> CRMWorkflowDB:
        wf = CRMWorkflowDB(
            merchant_id=merchant_id,
            assignee_id=assignee_id,
            notes=notes,
            due_date=due_date,
        )
        return await self.wf_repo.create(wf)

    async def get_workflow(self, merchant_id: str) -> CRMWorkflowDB:
        wf = await self.wf_repo.get_by_merchant(merchant_id)
        if not wf:
            raise NotFoundError("CRMWorkflow", merchant_id)
        return wf

    async def advance_workflow(
        self, merchant_id: str, new_stage: str, assignee_id: str | None = None
    ) -> CRMWorkflowDB:
        wf = await self.get_workflow(merchant_id)
        current = WorkflowStage(wf.stage)
        target = WorkflowStage(new_stage)
        allowed = VALID_WORKFLOW_TRANSITIONS.get(current, set())
        if target not in allowed:
            raise InvalidStateTransition("CRMWorkflow", wf.stage, new_stage)
        wf.stage = new_stage
        if assignee_id is not None:
            wf.assignee_id = assignee_id
        return await self.wf_repo.update(wf)

    # --- Reminders ---

    async def schedule_reminder(
        self,
        merchant_id: str,
        message: str,
        scheduled_at: datetime,
        channel: str = "log",
    ) -> ReminderDB:
        reminder = ReminderDB(
            merchant_id=merchant_id,
            message=message,
            scheduled_at=scheduled_at,
            channel=channel,
        )
        return await self.rem_repo.create(reminder)

    async def list_reminders(self, merchant_id: str) -> list[ReminderDB]:
        return await self.rem_repo.list_by_merchant(merchant_id)

    async def mark_reminder_sent(self, reminder_id: str) -> ReminderDB:
        reminder = await self.rem_repo.get_by_id(reminder_id)
        if not reminder:
            raise NotFoundError("Reminder", reminder_id)
        reminder.sent_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(reminder)
        return reminder
