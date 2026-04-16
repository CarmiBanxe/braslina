"""Repository for merchant register — all DB queries."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.register.db_models import MerchantDB


class MerchantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, merchant: MerchantDB) -> MerchantDB:
        self.db.add(merchant)
        await self.db.commit()
        await self.db.refresh(merchant)
        return merchant

    async def get_by_id(self, merchant_id: str) -> MerchantDB | None:
        return await self.db.get(MerchantDB, merchant_id)

    async def list_all(self, status: str | None = None) -> list[MerchantDB]:
        q = select(MerchantDB)
        if status:
            q = q.where(MerchantDB.status == status)
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def update(self, merchant: MerchantDB) -> MerchantDB:
        await self.db.commit()
        await self.db.refresh(merchant)
        return merchant

    async def delete(self, merchant: MerchantDB) -> None:
        await self.db.delete(merchant)
        await self.db.commit()
