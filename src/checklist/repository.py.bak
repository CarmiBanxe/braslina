"""Repository for checklists — all DB queries."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.checklist.db_models import CheckItemDB, ChecklistDB


class ChecklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, checklist: ChecklistDB) -> ChecklistDB:
        self.db.add(checklist)
        await self.db.commit()
        await self.db.refresh(checklist, ["items"])
        return checklist

    async def get_by_id(self, checklist_id: str) -> ChecklistDB | None:
        q = (
            select(ChecklistDB)
            .where(ChecklistDB.id == checklist_id)
            .options(selectinload(ChecklistDB.items))
        )
        result = await self.db.execute(q)
        return result.scalar_one_or_none()

    async def list_by_merchant(self, merchant_id: str) -> list[ChecklistDB]:
        q = (
            select(ChecklistDB)
            .where(ChecklistDB.merchant_id == merchant_id)
            .options(selectinload(ChecklistDB.items))
        )
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def get_item(self, item_id: str) -> CheckItemDB | None:
        return await self.db.get(CheckItemDB, item_id)

    async def update_item(self, item: CheckItemDB) -> CheckItemDB:
        await self.db.commit()
        await self.db.refresh(item)
        return item
