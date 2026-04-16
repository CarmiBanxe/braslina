"""Purchase service — business logic for test purchases."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import NotFoundError, ValidationError
from src.purchases.db_models import TestPurchaseDB
from src.purchases.repository import PurchaseRepository

VALID_RESULTS = {"passed", "failed", "partial"}


class PurchaseService:
    def __init__(self, db: AsyncSession):
        self.repo = PurchaseRepository(db)
        self.db = db

    def _validate_result(self, result: str) -> None:
        if result not in VALID_RESULTS:
            raise ValidationError(
                f"Invalid result '{result}'. Must be one of: {', '.join(sorted(VALID_RESULTS))}"
            )

    async def create_purchase(
        self,
        merchant_id: str,
        amount: float,
        currency: str,
        result: str,
        performed_by: str,
        screenshot_url: str | None = None,
        refund_tested: bool = False,
        refund_screenshot_url: str | None = None,
        notes: str | None = None,
    ) -> TestPurchaseDB:
        self._validate_result(result)
        purchase = TestPurchaseDB(
            merchant_id=merchant_id,
            amount=amount,
            currency=currency,
            result=result,
            performed_by=performed_by,
            screenshot_url=screenshot_url,
            refund_tested=refund_tested,
            refund_screenshot_url=refund_screenshot_url,
            notes=notes,
        )
        return await self.repo.create(purchase)

    async def get_purchase(self, purchase_id: str) -> TestPurchaseDB:
        purchase = await self.repo.get_by_id(purchase_id)
        if not purchase:
            raise NotFoundError("TestPurchase", purchase_id)
        return purchase

    async def list_purchases(self, merchant_id: str) -> list[TestPurchaseDB]:
        return await self.repo.list_by_merchant(merchant_id)

    async def get_summary(self, merchant_id: str) -> dict:
        """Return pass/fail/partial counts and last purchase date."""
        q = (
            select(
                TestPurchaseDB.result,
                func.count().label("count"),
            )
            .where(TestPurchaseDB.merchant_id == merchant_id)
            .group_by(TestPurchaseDB.result)
        )
        rows = await self.db.execute(q)
        counts = {r: 0 for r in VALID_RESULTS}
        for row in rows:
            counts[row.result] = row.count

        last_q = (
            select(func.max(TestPurchaseDB.performed_at))
            .where(TestPurchaseDB.merchant_id == merchant_id)
        )
        last_row = await self.db.execute(last_q)
        last_date = last_row.scalar()

        return {
            "merchant_id": merchant_id,
            "total": sum(counts.values()),
            "passed": counts["passed"],
            "failed": counts["failed"],
            "partial": counts["partial"],
            "last_purchase_at": last_date,
        }
