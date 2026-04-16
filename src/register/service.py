"""Register service — merchant lifecycle and status transitions."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import InvalidStateTransition, NotFoundError
from src.register.db_models import (
    VALID_STATUS_TRANSITIONS,
    MerchantDB,
    MerchantStatus,
    MerchantStatusLogDB,
)
from src.register.repository import MerchantRepository


class RegisterService:
    def __init__(self, db: AsyncSession):
        self.repo = MerchantRepository(db)
        self.db = db

    async def create_merchant(self, name: str, website: str, mcc: str) -> MerchantDB:
        merchant = MerchantDB(name=name, website=website, mcc=mcc)
        return await self.repo.create(merchant)

    async def get_merchant(self, merchant_id: str) -> MerchantDB:
        merchant = await self.repo.get_by_id(merchant_id)
        if not merchant:
            raise NotFoundError("Merchant", merchant_id)
        return merchant

    async def list_merchants(self, status: str | None = None) -> list[MerchantDB]:
        return await self.repo.list_all(status)

    async def change_status(
        self, merchant_id: str, new_status: str, changed_by: str | None = None, reason: str | None = None
    ) -> MerchantDB:
        merchant = await self.get_merchant(merchant_id)
        current = MerchantStatus(merchant.status)
        target = MerchantStatus(new_status)

        allowed = VALID_STATUS_TRANSITIONS.get(current, set())
        if target not in allowed:
            raise InvalidStateTransition("Merchant", merchant.status, new_status)

        log_entry = MerchantStatusLogDB(
            merchant_id=merchant.id,
            from_status=merchant.status,
            to_status=new_status,
            changed_by=changed_by,
            reason=reason,
        )
        self.db.add(log_entry)

        merchant.status = new_status
        return await self.repo.update(merchant)

    async def delete_merchant(self, merchant_id: str) -> None:
        merchant = await self.get_merchant(merchant_id)
        await self.repo.delete(merchant)
