"""Merchant checklist engine."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NEEDS_REVIEW = "needs_review"
    NOT_APPLICABLE = "not_applicable"


@dataclass(slots=True)
class ChecklistItem:
    code: str
    label: str
    status: CheckStatus
    notes: str = ""


@dataclass(slots=True)
class ChecklistResult:
    items: list[ChecklistItem]

    def failed_items(self) -> list[ChecklistItem]:
        return [item for item in self.items if item.status == CheckStatus.FAIL]

    def review_items(self) -> list[ChecklistItem]:
        return [item for item in self.items if item.status == CheckStatus.NEEDS_REVIEW]

    def is_blocked(self) -> bool:
        return bool(self.failed_items())


def default_merchant_checklist() -> ChecklistResult:
    return ChecklistResult(
        items=[
            ChecklistItem("mcc-match", "MCC matches business model", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("website-content", "Website content is sufficiently detailed", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("terms-policy", "Terms and policies are present", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("merchant-info", "Merchant identity and support info are present", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("payment-logos", "Card scheme logos are valid", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("checkout-3ds", "Checkout and 3DS behavior verified", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("test-purchase", "Test purchase evidence collected", CheckStatus.NEEDS_REVIEW),
            ChecklistItem("refund-check", "Refund flow verified", CheckStatus.NEEDS_REVIEW),
        ]
    )
