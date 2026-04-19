"""End-to-end onboarding workflow scaffold."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from src.agent.monitor import ScreenshotJob, run_job
from src.checklist.engine import ChecklistResult, default_merchant_checklist, evaluate
from src.register.models import MerchantRegisterEntry, MerchantStatus


@dataclass(slots=True)
class WorkflowResult:
    merchant: MerchantRegisterEntry
    checklist: ChecklistResult
    screenshot_path: Path
    webhook_payload: dict


def run_onboarding_workflow(
    merchant_id: str,
    legal_name: str,
    website: str,
    desired_mcc: str,
) -> WorkflowResult:
    merchant = MerchantRegisterEntry(
        merchant_id=merchant_id,
        legal_name=legal_name,
        website=website,
        desired_mcc=desired_mcc,
        status=MerchantStatus.IN_REVIEW,
        date_started_work=date.today(),
    )

    checklist_template = default_merchant_checklist()
    checklist = evaluate(["pending"] * len(checklist_template.items))
    screenshot_path = run_job(
        base_dir="storage/screenshots",
        job=ScreenshotJob(merchant_id=merchant_id, url=website),
    )
    merchant.schedule_periodic_review(90)

    webhook_payload = {
        "event": "merchant_onboarding_initialized",
        "merchant_id": merchant.merchant_id,
        "legal_name": merchant.legal_name,
        "website": merchant.website,
        "desired_mcc": merchant.desired_mcc,
        "status": merchant.status,
        "next_review_date": (
            merchant.next_review_date.isoformat()
            if merchant.next_review_date
            else None
        ),
        "checklist_items": checklist.total,
        "screenshot_path": str(screenshot_path),
    }

    return WorkflowResult(
        merchant=merchant,
        checklist=checklist,
        screenshot_path=screenshot_path,
        webhook_payload=webhook_payload,
    )


if __name__ == "__main__":
    result = run_onboarding_workflow(
        merchant_id="mrc_demo_001",
        legal_name="Demo Merchant Ltd",
        website="https://example.com",
        desired_mcc="5815",
    )
    print(result.webhook_payload)
