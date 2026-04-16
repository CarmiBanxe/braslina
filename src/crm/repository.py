"""Repository for CRM workflows and reminders."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crm.db_models import CRMWorkflowDB, ReminderDB


class WorkflowRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, workflow: CRMWorkflowDB) -> CRMWorkflowDB:
        self.db.add(workflow)
        await self.db.commit()
        await self.db.refresh(workflow)
        return workflow

    async def get_by_id(self, workflow_id: str) -> CRMWorkflowDB | None:
        return await self.db.get(CRMWorkflowDB, workflow_id)

    async def get_by_merchant(self, merchant_id: str) -> CRMWorkflowDB | None:
        q = select(CRMWorkflowDB).where(CRMWorkflowDB.merchant_id == merchant_id).order_by(CRMWorkflowDB.created_at.desc())
        result = await self.db.execute(q)
        return result.scalars().first()

    async def update(self, workflow: CRMWorkflowDB) -> CRMWorkflowDB:
        await self.db.commit()
        await self.db.refresh(workflow)
        return workflow


class ReminderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, reminder: ReminderDB) -> ReminderDB:
        self.db.add(reminder)
        await self.db.commit()
        await self.db.refresh(reminder)
        return reminder

    async def get_by_id(self, reminder_id: str) -> ReminderDB | None:
        return await self.db.get(ReminderDB, reminder_id)

    async def list_by_merchant(self, merchant_id: str) -> list[ReminderDB]:
        q = select(ReminderDB).where(ReminderDB.merchant_id == merchant_id).order_by(ReminderDB.scheduled_at.desc())
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def list_pending(self) -> list[ReminderDB]:
        q = select(ReminderDB).where(ReminderDB.sent_at.is_(None)).order_by(ReminderDB.scheduled_at.asc())
        result = await self.db.execute(q)
        return list(result.scalars().all())
