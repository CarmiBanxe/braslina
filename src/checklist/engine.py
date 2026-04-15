"""Merchant Checklist Engine — template-based with auto-verify support."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Callable, Awaitable


class CheckStatus(StrEnum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(slots=True)
class CheckItem:
    id: str
    name: str
    description: str
    auto_verifiable: bool = False
    status: CheckStatus = CheckStatus.PENDING
    verified_at: datetime | None = None
    evidence_url: str | None = None
    notes: str | None = None

    def mark(self, status: CheckStatus, evidence: str | None = None, notes: str | None = None):
        self.status = status
        self.verified_at = datetime.utcnow()
        if evidence:
            self.evidence_url = evidence
        if notes:
            self.notes = notes


@dataclass(slots=True)
class ChecklistTemplate:
    id: str
    name: str
    version: str
    items: list[CheckItem] = field(default_factory=list)


@dataclass(slots=True)
class MerchantChecklist:
    id: str
    merchant_id: str
    template_id: str
    items: list[CheckItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

    @property
    def progress(self) -> float:
        done = sum(1 for i in self.items if i.status in (CheckStatus.PASSED, CheckStatus.SKIPPED))
        return round(done / len(self.items) * 100, 1) if self.items else 0.0

    @property
    def is_complete(self) -> bool:
        return all(i.status != CheckStatus.PENDING for i in self.items)

    def complete_if_ready(self):
        if self.is_complete and not self.completed_at:
            self.completed_at = datetime.utcnow()


# --- Default Sales checklist template ---

SALES_CHECKLIST = ChecklistTemplate(
    id="tpl_sales_v1",
    name="Sales Onboarding Checklist",
    version="1.0",
    items=[
        CheckItem(id="chk_mcc", name="MCC Verification", description="Verify merchant MCC code is correct", auto_verifiable=True),
        CheckItem(id="chk_tc", name="Terms & Conditions", description="Website has visible T&C page", auto_verifiable=True),
        CheckItem(id="chk_logo", name="Payment System Logos", description="Visa/MC logos displayed on payment page", auto_verifiable=True),
        CheckItem(id="chk_3ds", name="3D Secure", description="3D Secure is enabled for card payments", auto_verifiable=False),
        CheckItem(id="chk_refund", name="Refund Policy", description="Clear refund policy published on website", auto_verifiable=True),
        CheckItem(id="chk_contact", name="Contact Info", description="Valid contact information on website", auto_verifiable=True),
        CheckItem(id="chk_ssl", name="SSL Certificate", description="Website uses valid HTTPS", auto_verifiable=True),
        CheckItem(id="chk_privacy", name="Privacy Policy", description="GDPR-compliant privacy policy present", auto_verifiable=True),
    ],
)


if __name__ == "__main__":
    import copy
    cl = MerchantChecklist(
        id="mcl_001", merchant_id="mrc_001", template_id=SALES_CHECKLIST.id,
        items=copy.deepcopy(SALES_CHECKLIST.items),
    )
    cl.items[0].mark(CheckStatus.PASSED, evidence="MCC 5815 confirmed")
    cl.items[1].mark(CheckStatus.PASSED)
    cl.items[6].mark(CheckStatus.PASSED, evidence="https cert valid until 2027")
    print(f"Progress: {cl.progress}%  Complete: {cl.is_complete}")
