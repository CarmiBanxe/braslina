"""Merchant onboarding register domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import StrEnum


class MerchantStatus(StrEnum):
    NEW = "new"
    IN_REVIEW = "in_review"
    CHANGES_REQUIRED = "changes_required"
    APPROVED = "approved"
    LIVE = "live"
    REJECTED = "rejected"
    PERIODIC_REVIEW = "periodic_review"


@dataclass(slots=True)
class MerchantRegisterEntry:
    merchant_id: str
    legal_name: str
    website: str
    desired_mcc: str
    status: MerchantStatus
    date_started_work: date
    next_review_date: date | None = None
    expected_turnover_eur: float | None = None

    def schedule_periodic_review(self, days: int = 90) -> date:
        self.next_review_date = self.date_started_work + timedelta(days=days)
        return self.next_review_date


if __name__ == "__main__":
    entry = MerchantRegisterEntry(
        merchant_id="mrc_001",
        legal_name="Demo Merchant Ltd",
        website="https://example.com",
        desired_mcc="5815",
        status=MerchantStatus.IN_REVIEW,
        date_started_work=date(2026, 4, 15),
        expected_turnover_eur=5000.0,
    )
    print("next_review_date:", entry.schedule_periodic_review())
