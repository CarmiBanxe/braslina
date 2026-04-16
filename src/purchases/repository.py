"""Repository for test purchases — all DB queries."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.purchases.db_models import TestPurchaseDB


class PurchaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, purchase: TestPurchaseDB) -> TestPurchaseDB:
        self.db.add(purchase)
        await self.db.commit()
        await self.db.refresh(purchase)
        return purchase

    async def get_by_id(self, purchase_id: str) -> TestPurchaseDB | None:
        return await self.db.get(TestPurchaseDB, purchase_id)

    async def list_by_merchant(self, merchant_id: str) -> list[TestPurchaseDB]:
        q = (
            select(TestPurchaseDB)
            .where(TestPurchaseDB.merchant_id == merchant_id)
            .order_by(TestPurchaseDB.performed_at.desc())
        )
        result = await self.db.execute(q)
        return list(result.scalars().all())
