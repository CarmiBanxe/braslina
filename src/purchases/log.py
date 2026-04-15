"""Test Purchase Log — logging test purchases with screenshot evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class PurchaseResult(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


@dataclass(slots=True)
class TestPurchase:
    id: str
    merchant_id: str
    amount: float
    currency: str
    result: PurchaseResult
    performed_by: str
    performed_at: datetime = field(default_factory=datetime.utcnow)
    screenshot_url: str | None = None
    refund_tested: bool = False
    refund_screenshot_url: str | None = None
    notes: str | None = None


@dataclass
class TestPurchaseLog:
    merchant_id: str
    entries: list[TestPurchase] = field(default_factory=list)

    def add(self, purchase: TestPurchase):
        self.entries.append(purchase)

    @property
    def success_count(self) -> int:
        return sum(1 for e in self.entries if e.result == PurchaseResult.SUCCESS)

    @property
    def refund_tested_count(self) -> int:
        return sum(1 for e in self.entries if e.refund_tested)


if __name__ == "__main__":
    log = TestPurchaseLog(merchant_id="mrc_001")
    log.add(TestPurchase(
        id="tp_001", merchant_id="mrc_001", amount=9.99,
        currency="EUR", result=PurchaseResult.SUCCESS,
        performed_by="qa_agent", refund_tested=True,
    ))
    log.add(TestPurchase(
        id="tp_002", merchant_id="mrc_001", amount=49.99,
        currency="EUR", result=PurchaseResult.FAILED,
        performed_by="qa_agent",
    ))
    print(f"Purchases: {len(log.entries)}  Success: {log.success_count}  Refunds tested: {log.refund_tested_count}")
