from datetime import date

from src.register.models import MerchantRegisterEntry, MerchantStatus


def test_schedule_periodic_review_default_90_days():
    entry = MerchantRegisterEntry(
        merchant_id="mrc_001",
        legal_name="Demo Merchant Ltd",
        website="https://example.com",
        desired_mcc="5815",
        status=MerchantStatus.IN_REVIEW,
        date_started_work=date(2026, 4, 15),
    )
    assert entry.schedule_periodic_review().isoformat() == "2026-07-14"


def test_register_entry_keeps_expected_fields():
    entry = MerchantRegisterEntry(
        merchant_id="mrc_002",
        legal_name="Merchant Two Ltd",
        website="https://merchant-two.example",
        desired_mcc="5999",
        status=MerchantStatus.NEW,
        date_started_work=date(2026, 4, 16),
        expected_turnover_eur=12000.0,
    )
    assert entry.expected_turnover_eur == 12000.0
    assert entry.status == MerchantStatus.NEW
