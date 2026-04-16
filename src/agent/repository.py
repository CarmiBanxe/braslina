"""Repository for website monitor snapshots — all DB queries."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.db_models import SnapshotDB


class SnapshotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, snapshot: SnapshotDB) -> SnapshotDB:
        self.db.add(snapshot)
        await self.db.commit()
        await self.db.refresh(snapshot)
        return snapshot

    async def list_by_merchant(self, merchant_id: str) -> list[SnapshotDB]:
        q = (
            select(SnapshotDB)
            .where(SnapshotDB.merchant_id == merchant_id)
            .order_by(SnapshotDB.created_at.desc())
        )
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def get_latest(self, merchant_id: str) -> SnapshotDB | None:
        q = (
            select(SnapshotDB)
            .where(SnapshotDB.merchant_id == merchant_id)
            .order_by(SnapshotDB.created_at.desc())
            .limit(1)
        )
        result = await self.db.execute(q)
        return result.scalar_one_or_none()
